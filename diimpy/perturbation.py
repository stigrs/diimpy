# Copyright (c) 2025 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import numpy as np

"""
Class for creating perturbations for the Dynamic Inoperability Input-Output 
Model.

TODO:
    Implement several types of perturbations.
"""
class Perturbation:

    def __init__(self, config, infra):
        self.__infra = infra
        self.__pindex = []
        self.config = {
            "pinfra": [],
            "cvalue": [],
        }
        if "Perturbation" in config:
            self.config.update(config["Perturbation"])
            if len(self.config["pinfra"]) != len(self.config["cvalue"]):
                raise Exception("bad sizes")
            self._init_perturbation()

    def _init_perturbation(self):
        self.c0 = np.zeros(len(self.__infra))
        if self.config["pinfra"]:
            self.__pindex = []
            for item in self.config["pinfra"]:
                self.__pindex.append(self.__infra.index(item))
        if "ptime" not in self.config:
            self.config["ptime"] = []
            for _ in self.config["pinfra"]:
                self.config["ptime"].append([0, 0])

    def set_perturbation(self, pinfra, ptime=None, cvalue=None):
        self.config["pinfra"] = pinfra
        if ptime:
            self.config["ptime"] = ptime
        if cvalue:
            self.config["cvalue"] = cvalue
        self._init_perturbation()

    def cstar(self, time=0):
        """Return perturbation c*(t)."""
        ct = self.c0
        for i, _ in enumerate(self.config["ptime"]):
            if (
                time >= self.config["ptime"][i][0]
                and time <= self.config["ptime"][i][1]
            ):
                ct[self.__pindex[i]] = self.config["cvalue"][i]
        return ct
