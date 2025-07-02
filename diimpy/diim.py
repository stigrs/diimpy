# Copyright (c) 2025 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import math
import numpy as np
import pandas as pd

from scipy.linalg import expm
from diimpy.perturbation import Perturbation 
from diimpy.mapping import map_to_interdep

"""
DIIM provides the Demand-Reduction and Recovery Dynamic Inoperability
Input-Output Model (DIIM) for interdependent infrastructures as described
in the papers:

 - Haimes, Y. Y., Horowitz, B. M., Lambert, J. H., Santos, J. R., Lian, C. &
   Crowther, K. G. (2005). Inoperability input-output model for interdependent
   infrastructure sectors. I: Theory and methodology. Journal of
   Infrastructure Systems, 11, 67-79.
 
 - Lian, C. & Haimes, Y. Y. (2006). Managing the Risk of Terrorism to
   Interdependent Infrastructure Systems Through the Dynamic Inoperability
   Input-Output Model. Systems Engineering, 9, 241-258.
 
DIIM also provides the Static Demand-Driven and Supply-Driven Inoperability
Input-Output Models (IIM) for interdependent infrastructures as described in
the papers:

 - Haimes, Y. Y & Jiang, P. (2001). Leontief-based model of risk in complex
   interconnected infrastructures. Journal of Infrastructure Systems, 7, 1-12.
 
 - Haimes, Y. Y., Horowitz, B. M., Lambert, J. H., Santos, J. R., Lian, C. &
   Crowther, K. G. (2005). Inoperability input-output model for interdependent
   infrastructure sectors. I: Theory and methodology. Journal of
   Infrastructure Systems, 11, 67-79.
 
 - Leung, M., Haimes, Y. Y. & Santos, J. R. (2007). Supply- and output-side
   extensions to the inoperability input-output model for interdependent
   infrastructures. Journal of Infrastructure Systems, 13, 299-310.
 
 - Santos, J. R. & Haimes, Y. Y. (2004). Modeling the demand reduction
   input-output (I-O) inoperability due to terrorism of interconnected
   infrastructures. Risk Analysis, 24, 1437-1451.
 
 - Setola, R., De Porcellinis, S. & Sforna, M. (2009). Critical infrastructure
   dependency assessment using the input-output inoperability model.
   International Journal of Critical Infrastructure Protection, 2, 170-178.
"""
class DIIM:
    """Class providing the Dynamic Inoperability Input-Output Model."""

    def __init__(self, config={}):
        # Set default values:
        self.config = {
            "mode": "demand",  # type of calculation mode
            "matrix_type": "interdependency",  # type of interdependency matrix
            "infra": [],  # list of infrastructures
            "lambda": 0.01,  # q(tau) value
            "time_steps": 0,  # number of time steps
            "map_scale": "5-point", # mapping consequences to A* matrix
            "datafile": None,  # file with interdependency matrix etc.
            "amat_sheet_name": "A_matrix",  # name of Excel sheet with A* matrix
            "tau_sheet_name": None, # name of Excel sheet with tau values
            "kmat_sheet_name": None, # name of Excel sheet with K matrix
            "q0_sheet_name": None, # name of Excel sheet with q(0) values
        }
        self.config.update(config["DIIM"])
        self.infra = [] 
        self.xoutput = None
        self.io_table = None
        self.amat = None
        self.astar = None
        self.smat = None
        self.q0 = None
        self.__tau = None
        self.__kmat = None
        self.__KMAT_MAX = 0.9999 # k[i] = [0, 1)

        self._read_io_table()
        self._calc_leontief_coefficients()
        self._calc_interdependency_matrix()
        self._init_tau_values()
        self._init_k_matrix()
        self._init_q0()

        self.perturb = Perturbation(config, self.infra)

    def __len__(self):
        """Return number of infrastructures."""
        return len(self.infra)

    def _read_io_table(self):
        """Read input-output table or A* matrix from Excel file (xlsx).

        Note:
            If input-output table is provided, last row must provide 
            total outputs.
        """
        df = pd.read_excel(
            self.config["datafile"], sheet_name=self.config["amat_sheet_name"]
        )
        self.infra = df.columns.tolist()
        io_tmp = df.to_numpy()

        if (
            self.config["matrix_type"] == "interdependency"
            or self.config["matrix_type"] == "consequence"
        ):
            self.io_table = io_tmp
        elif self.config["matrix_type"] == "input-output":
            self.xoutput = io_tmp[-1, :]
            self.io_table = io_tmp[:-1, :]
        else:
            raise Exception("bad matrix_type: " + self.config["matrix_type"])

    def _calc_leontief_coefficients(self):
        # Calculate Leontief technical coefficients matrix (A) from I-O table.
        #
        # Algorithm:
        #   Santos & Haimes (2004), eq. 2.
        #
        n = self.__len__()
        self.amat = np.zeros(shape=(n, n)) 
        if self.config["matrix_type"] == "input-output":
            for i in range(n):
                for j in range(n):
                    if self.xoutput[j] != 0:
                        self.amat[i, j] = self.io_table[i, j] / self.xoutput[j]

    def _calc_interdependency_matrix(self):
        # Calculate demand-driven or supply-driven interdependency matrix
        # and the S matrix from technical coefficients.
        #
        # Algorithm:
        #  Santos & Haimes (2004), eq. 28. (A* matrix)
        #  Leung et al. (2007), p. 301 (A^S matrix)
        #  Setola et al. (2009), eq. 7. (S matrix)
        #
        n = self.__len__()
        self.astar = np.zeros(shape=(n, n))
        if self.config["matrix_type"] == "input-output":
            if self.config["mode"] == "supply":
                self.astar = np.transpose(self.amat) # Leung (2007), p. 301
            else: # demand-driven
                # The algorithm:
                #   pmat = np.identity(n) * self.xoutput
                #   pinv = np.linalg.inv(pmat)
                #   self.astar = np.matmul(self.amat, pmat)
                #   self.astar = np.matmul(pinv, self.astar)
                # may create singular matrix if x_i == 0.
                for i in range(n):
                    for j in range(n):
                        if self.xoutput[j] != 0:
                            self.astar[i, j] = self.io_table[i, j] / self.xoutput[j]
        elif self.config["matrix_type"] == "consequence":
            self.astar = map_to_interdep(self.io_table, self.config["map_scale"])
        else: # interdependency matrix provided
            self.astar = self.io_table
        self._check_stability()
        self.smat = np.linalg.inv(np.identity(n) - self.astar)

    def _check_stability(self):
        # Check if the dominant eigenvalue of matrix A* is smaller in absolute
        # value than 1.
        #
        # Reference:
        #   Setola et al. (2009), eq. 6.
        #
        evals, _ = np.linalg.eig(self.astar)
        idx = evals.argsort()[::-1] # ascending order
        evals = evals[idx]
        lambda_0 = np.abs(np.real(evals.max()))
        if lambda_0 >= 1:
            raise Exception("A* is not stable, dominant eigenvalue is " + str(lambda_0))

    def _init_tau_values(self):
        # Initialize tau values by reading from xlsx file.
        if self.config["tau_sheet_name"]:
            df = pd.read_excel(
                self.config["datafile"], sheet_name=self.config["tau_sheet_name"]
            )
            self.__tau = df.to_numpy()[0]
        else:
            self.__tau = []

    def _init_k_matrix(self):
        # Initialize K matrix by reading from xlxs file. Set default values if
        # no file is provided.
        if self.config["kmat_sheet_name"]:
            df = pd.read_excel(
                self.config["datafile"], sheet_name=self.config["kmat_sheet_name"]
            )
            self.__kmat = df.to_numpy()
            # fix bad input values
            self.__kmat[self.__kmat > 1.0] = self.__KMAT_MAX # upper limit
            self.__kmat[self.__kmat < 0.0] = 0.0 # lower limit
            n = self.__len__()
            if len(self.__kmat[0]) == n:
                self.__kmat = np.multiply(np.identity(n), self.__kmat)
            else:
                raise Exception("bad size of K matrix")
        elif self.__tau:
            self._calc_k_matrix()
        else: # set K matrix to identity matrix
            self.__kmat = np.identity(self.__len__())

    def _calc_k_matrix(self):
        # Calculate K matrix from lambda and tau values.
        self.__kmat = (-math.log(self.config["lambda"]) / self.__tau) / (
            1.0 - np.diag(self.astar)
        )
        self.__kmat[self.__kmat > 1.0] = self.__KMAT_MAX # upper limit
        self.__kmat[self.__kmat < 0.0] = 0.0 # lower limit

    def _init_q0(self):
        # Initialize q(0) data by reading from xlsx file. Set default values
        # if no file is provided.
        if self.config["q0_sheet_name"]:
            df = pd.read_excel(
                self.config["datafile"], sheet_name=self.config["q0_sheet_name"]
            )
            self.q0 = df.to_numpy()[0]
            if len(self.q0) != self.__len__():
                raise Exception("bad size of q(0)")
            # fix bad input values
            self.q0[self.q0 > 1.0] = 1.0 # upper limit
            self.q0[self.q0 < 0.0] = 0.0 # lower limit
        else:
            self.q0 = np.zeros(self.__len__())

    def set_perturbation(self, pinfra, ptime=None, cvalue=None):
        self.perturb.set_perturbation(pinfra, ptime, cvalue)

    def dependency(self):
        """Calculate dependency index."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 3.
        #
        # Note:
        #   Only defined for demand-driven DIIM.
        #
        if self.config["mode"] == "demand":
            n = self.__len__()
            delta = np.zeros(n)
            for i in range(n):
                di = 0.0
                for j in range(n):
                    if j != i:
                        di += self.astar[i, j]
                delta[i] = di
            return delta / (n - 1.0)
        else:
            return None

    def influence(self):
        """Calculate influence gain."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 4.
        #
        # Note:
        #   Only defined for demand-driven DIIM.
        #
        if self.config["mode"] == "demand":
            n = self.__len__()
            rho = np.zeros(n)
            for j in range(n):
                rj = 0.0
                for i in range(n):
                    if i != j:
                        rj += self.astar[i, j]
                rho[j] = rj
            return rho / (n - 1.0)
        else:
            return None

    def overall_dependency(self):
        """Calculate overall dependency index."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 9.
        #
        # Note:
        #   Only defined for demand-driven IIM.
        #
        if self.config["mode"] == "demand":
            n = self.__len__()
            delta = np.zeros(n)
            for i in range(n):
                di = 0.0
                for j in range(n):
                    if j != i:
                        di += self.smat[i, j]
                delta[i] = di
            return delta / (n - 1.0)
        else:
            return None

    def overall_influence(self):
        """Calculate influence gain."""
        #
        # Algorithm:
        #   Setola et al. (2009), eq. 10.
        #
        # Note:
        #   Only defined for demand-driven IIM.
        #
        if self.config["mode"] == "demand":
            n = self.__len__()
            rho = np.zeros(n)
            for j in range(n):
                rj = 0.0
                for i in range(n):
                    if i != j:
                        rj += self.smat[i, j]
                rho[j] = rj
            return rho / (n - 1.0)
        else:
            return None

    def interdependency_index(self, isector, jsector, order=1):
        """Return n-th order interdependency index between two infrastructures."""
        try:
            i = self.infra.index(isector)
            j = self.infra.index(jsector)
            res = np.linalg.matrix_power(self.astar, order)
            return res[i, j]
        except ValueError:
            return None

    def max_nth_order_interdependency(self, n=1):
        """Return maximum nth-order interdependency index for each sector."""
        assert n >= 1
        amat = np.linalg.matrix_power(self.astar, n)
        res = []
        for i in range(self.__len__()):
            j = np.argmax(amat[i, :], axis=0)
            tmp = [self.infra[i], self.infra[j], amat[i, j]]
            res.append(tmp)
        return res

    def inoperability(self):
        """Calculate inoperability for the infrastructure functions at
        equilibrium."""
        #
        # Algorithm:
        #   Haimes & Jiang (2001), eq. 14.
        #   Haimes et al. (2005), eq. 38.
        #
        q = np.matmul(self.smat, self.perturb.cstar())
        q[q > 1.0] = 1.0 # fix roundoff errors
        return q

    def dynamic_inoperability(self):
        """Calculate demand-reduction dynamic inoperability of the 
        infrastructure functions."""
        #
        # Algorithm:
        #   Haimes et al. (2005), eq. 51.
        #   Lian & Haimes (2006), eq. 21.
        #
        n = self.__len__()
        nt = self.config["time_steps"]
        if self.config["time_steps"] == 0:
            nt = 1
        qt = np.zeros(shape=(nt, n + 1))
        qk = self.q0

        for k in range(1, self.config["time_steps"]):
            qk = (
                np.matmul(
                    self.__kmat,
                    (np.matmul(self.astar, qk) + self.perturb.cstar(k) - qk),
                )
                + qk
            )
            qk[qk > 1.0] = 1.0 # upper limit (fix roundoff errors)
            qt[k, 0] = k
            qt[k, 1:] = qk
        return qt

    def dynamic_recovery(self):
        """Calculate the dynamic recovery of the infrastructure sectors."""
        #
        # Algorithm:
        #   Lian & Haimes (2006), eq. 26.
        #
        n = self.__len__()
        nt = self.config["time_steps"]
        if self.config["time_steps"] == 0:
            nt = 1

        qt = np.zeros((nt, n + 1))
        qk = np.zeros(n)
        tmp = np.matmul(self.__kmat, np.identity(n) - self.astar)
        for k in range(1, self.config["time_steps"]):
            qk = np.matmul(expm(-tmp * k), self.q0)
            qk[qk < 0.0] = 0.0  # lower limit (fix roundoff errors)
            qt[k, 0] = k
            qt[k, 1:] = qk
        return qt

    def impact(self, qt):
        """Compute impact by integrating q(t)."""
        qtot = []
        for j in range(1, np.size(qt, 1)):
            qtot.append(np.trapezoid(qt[:, j]))
        return np.array(qtot)
