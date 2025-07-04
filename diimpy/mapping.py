# Copyright (c) 2025 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import numpy as np

def _map_to_interdep(consequence, scale):
    """Mapping of consequences to interdependency values."""
    #
    # Algorithm:
    #   Qualitative consequence assessments on an N-point scale are
    #   mapped to interdependencies values using a power law distribution:
    #
    #     a^{\star}_{ij} = a * C^b
    #
    #   where C is the consequence score. The a and b values are fitted to
    #   the data in Table 1 in Setola (2009).
    #
    # References:
    # - Setola, R., De Porcellinis, S. & Sforna, M. (2009). Critical
    #   infrastructure dependency assessment using the input-output
    #   inoperability model. International Journal of Critical Infrastructure
    #   Protection, 2, 170-178.
    #
    # Note:
    #   5-point is default
    #
    a = 0.008 
    b = 2.569323442 
    if scale == "4-point":
        a = 0.01
        b = 2.821928095
    return a * np.power(consequence, b)

map_to_interdep = np.vectorize(_map_to_interdep)
