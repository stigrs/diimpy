# Copyright (c) 2025 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import os
import unittest
import numpy as np
import diimpy.diim as dpd

class TestDIIM(unittest.TestCase):

    def test_case1(self):
        # Correct answer (Haimes & Jiang, 2001):
        # --------------------------------------
        # For c = [0.0, 0.6], q = [0.571, 0.714]
        qans = [0.571, 0.714]

        fname = os.path.join("tests", "test_case1.xlsx")
        config = {
            "DIIM": {
                "table": "interdependency",
                "mode": "Demand",
                "datafile": fname
            },
            "Perturbation": {
                "pinfra": ["Sector2"],
                "cvalue": [0.6] 
            }
        }
        model = dpd.DIIM(config)
        q = model.inoperability()

        self.assertTrue(np.allclose(q, qans, atol=0.001))

    def test_case2(self):
        # Correct answer (Haimes & Jiang, 2001):
        # --------------------------------------
        # For c = [0.0, 0.5, 0.0, 0.0], q = [0.70, 0.78, 1, 1]
        qans = [0.70, 0.78, 1.0, 1.0]

        fname = os.path.join("tests", "test_case2.xlsx")
        config = {
            "DIIM": {
                "table": "interdependency",
                "mode": "demand",
                "datafile": fname
            },
            "Perturbation": {
                "pinfra": ["Sector2"],
                "cvalue": [0.5] 
            }
        }
        model = dpd.DIIM(config)
        q = model.inoperability()

        self.assertTrue(np.allclose(q, qans, atol=0.01))

    def test_case3(self):
        # Correct answer:
        # ---------------
        # For c = [0.0, 0.0, 0.12], q = [0.04, 0.02, 0.14]
        qans = [0.04, 0.02, 0.14]

        fname = os.path.join("tests", "test_case3.xlsx")
        config = {
            "DIIM": {
                "table": "interdependency",
                "mode": "demand",
                "datafile": fname
            },
            "Perturbation": {
                "pinfra": ["SectorC"],
                "cvalue": [0.12] 
            }
        }
        model = dpd.DIIM(config)
        q = model.inoperability()

        self.assertTrue(np.allclose(q, qans, atol=0.01))

    def test_case4(self):
        # Correct answer:
        # ---------------
        # Xu et al. (2011), eq. 31.
        a_ans = [[0.14, 0.17, 0.26, 0.14],
                 [0.11, 0.20, 0.32, 0.28],
                 [0.20, 0.10, 0.26, 0.14],
                 [0.14, 0.17, 0.10, 0.28]]

        fname = os.path.join("tests", "test_case4.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "input-output",
                "mode": "supply",
                "datafile": fname,
                "amat_sheet_name": "IO_table",
            },
            "Perturbation": {
                "pinfra": ["Electric"],
                "cvalue": [0.0] 
            }
        }
        model = dpd.DIIM(config)
        self.assertTrue(np.allclose(a_ans, model.amat, atol=0.015))

    def test_case5(self):
        # Correct answer:
        # ---------------
        # Xu et al. (2011), eq. 34.
        a_ans = [[0.14, 0.11, 0.20, 0.14],
                 [0.17, 0.20, 0.10, 0.17],
                 [0.26, 0.32, 0.26, 0.10],
                 [0.14, 0.28, 0.14, 0.28]]

        fname = os.path.join("tests", "test_case5.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "input-output",
                "mode": "supply",
                "datafile": fname,
                "amat_sheet_name": "IO_table",
            },
            "Perturbation": {
                "pinfra": ["Electric"],
                "cvalue": [0.0] 
            }
        }
        model = dpd.DIIM(config)
        self.assertTrue(np.allclose(a_ans, model.astar, atol=0.015))

    def test_case6(self):
        # Correct answer:
        # ---------------
        # Lian and Haimes (2006).
        q_ans = [0.066, 0.112]

        fname = os.path.join("tests", "test_case6.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "interdependency",
                "mode": "demand",
                "datafile": fname,
            },
            "Perturbation": {
                "pinfra": ["Sector2"],
                "cvalue": [0.1] 
            }
        }
        model = dpd.DIIM(config)
        q = model.inoperability()

        self.assertTrue(np.allclose(q_ans, q, atol=0.001))

    def test_case7(self):
        # Numpy calculations:
        ans1 = 0.9
        ans2 = 0.288
        ans3 = 0.324
        ans4 = 0.0

        ans_max = [0.324, 0.144, 0.36, 0.36]

        fname = os.path.join("tests", "test_case7.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "interdependency",
                "mode": "demand",
                "datafile": fname,
            },
        }
        model = dpd.DIIM(config)
        res1 = model.interdependency_index("Sector3", "Sector2", 2)
        res2 = model.interdependency_index("Sector3", "Sector2", 3)
        res3 = model.interdependency_index("Sector1", "Sector2", 3)
        res4 = model.interdependency_index("Sector4", "Sector4", 3)

        self.assertTrue(np.allclose(ans1, res1, atol=0.001))
        self.assertTrue(np.allclose(ans2, res2, atol=0.001))
        self.assertTrue(np.allclose(ans3, res3, atol=0.001))
        self.assertTrue(np.allclose(ans4, res4, atol=0.001))

        res_max = model.max_nth_order_interdependency(3)
        res_max = [row[2] for row in res_max[:]]
        self.assertTrue(np.allclose(ans_max, res_max, atol=0.001))

    def test_case8(self):
        # Correct answer:
        # ---------------
        # Lian & Haimes (2006).
        q_ans = [0.066, 0.112]

        fname = os.path.join("tests", "test_case8.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "interdependency",
                "mode": "demand",
                "time_steps": 100,
                "datafile": fname,
                "kmat_sheet_name": "K_matrix" 
            },
            "Perturbation": {
                "pinfra": ["Sector2"],
                "ptime": [[0, 100]],
                "cvalue": [0.1],
            }
        }
        model = dpd.DIIM(config)
        qt = model.dynamic_inoperability()

        self.assertTrue(np.allclose(q_ans, qt[-1, 1:], atol=0.001))

    def test_case9(self):
        qans = [0.0, 0.0]

        fname = os.path.join("tests", "test_case8_amat.csv")
        kfile = os.path.join("tests", "test_case8_kmat.csv")
        qfile = os.path.join("tests", "test_case8_q0.csv")
        config = {
            "psector": ["Sector2"],
            "cvalue": [0.1],
            "table": "A",
            "mode": "Demand",
            "kmat_file": kfile,
            "q0_file": qfile
        }
        fname = os.path.join("tests", "test_case9.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "interdependency",
                "mode": "demand",
                "time_steps": 100,
                "datafile": fname,
                "kmat_sheet_name": "K_matrix",
                "q0_sheet_name": "q0_data" 
            },
            "Perturbation": {
                "pinfra": ["Sector2"],
                "cvalue": [0.1],
            }
        }
        model = dpd.DIIM(config)
        qt = model.dynamic_recovery()

        self.assertTrue(np.allclose(qans, qt[-1, 1:], atol=0.001))

    def test_case10(self):
        # Integrated using Numpy:
        qtot_ans = [5.78342065, 10.49188014]

        fname = os.path.join("tests", "test_case10.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "interdependency",
                "datafile": fname,
                "amat_sheet_name": "A_matrix",
                "kmat_sheet_name": "K_matrix",
                "time_steps": 100,
            },
            "Perturbation": {
                "pinfra": ["Sector2"],
                "cvalue": [0.1],
                "ptime": [[0, 30]],
            },
        }
        model = dpd.DIIM(config)
        qt = model.dynamic_inoperability()
        qtot = model.impact(qt)

        self.assertTrue(np.allclose(qtot_ans, qtot, atol=0.001))

    def test_case11(self):
        # Correct answer:
        a_ans = [
            [0.0000, 0.2818, 0.5000, 0.0475],
            [0.0080, 0.0000, 0.0080, 0.2818],
            [0.1346, 0.0475, 0.0000, 0.1346],
            [0.0475, 0.1346, 0.0475, 0.0000],
        ]

        fname = os.path.join("tests", "test_case11.xlsx")
        config = {
            "DIIM": {
                "matrix_type": "consequence",
                "mode": "demand",
                "datafile": fname,
                "amat_sheet_name": "Consequence",
            },
            "Perturbation": {
                "pinfra": ["Electric"],
                "cvalue": [0.0] 
            }
        }
        model = dpd.DIIM(config)
        self.assertTrue(np.allclose(a_ans, model.astar, atol=0.0001))
