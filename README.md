# Dynamic Inoperability Input-Output Model for Python (DIIMPY)

DIIMPY provides the Demand-Reduction and Recovery Dynamic Inoperability
Input-Output Model (DIIM) for interdependent functions as described in
the papers:

* Haimes, Y. Y., Horowitz, B. M., Lambert, J. H., Santos, J. R., Lian, C. &
  Crowther, K. G. (2005). Inoperability input-output model for interdependent
  infrastructure sectors. I: Theory and methodology. Journal of
  Infrastructure Systems, 11, 67-79.

* Lian, C. & Haimes, Y. Y. (2006). Managing the Risk of Terrorism to
  Interdependent Infrastructure Systems Through the Dynamic Inoperability
  Input-Output Model. Systems Engineering, 9, 241-258.

DIIMPY also provides the Static Demand-Driven and Supply-Driven Inoperability
Input-Output Models (IIM) for interdependent functions as described in the
papers:

* Haimes, Y. Y & Jiang, P. (2001). Leontief-based model of risk in complex
  interconnected infrastructures. Journal of Infrastructure Systems, 7, 1-12.

* Haimes, Y. Y., Horowitz, B. M., Lambert, J. H., Santos, J. R., Lian, C. &
  Crowther, K. G. (2005). Inoperability input-output model for interdependent
  infrastructure sectors. I: Theory and methodology. Journal of
  Infrastructure Systems, 11, 67-79.

* Leung, M., Haimes, Y. Y. & Santos, J. R. (2007). Supply- and output-side
  extensions to the inoperability input-output model for interdependent
  infrastructures. Journal of Infrastructure Systems, 13, 299-310.

* Santos, J. R. & Haimes, Y. Y. (2004). Modeling the demand reduction
  input-output (I-O) inoperability due to terrorism of interconnected
  infrastructures. Risk Analysis, 24, 1437-1451.

* Setola, R., De Porcellinis, S. & Sforna, M. (2009). Critical infrastructure
  dependency assessment using the input-output inoperability model.
  International Journal of Critical Infrastructure Protection, 2, 170-178.

## Licensing

DIIMPY is released under the [MIT](LICENSE) license.

## Quick Start 

### Requirements

* [CMake](https://cmake.org) 3.13
* [OpenBLAS](https://www.openblas.net/) (Intel MKL is recommended)

### Obtaining the Source Code

The source code can be obtained from

        git clone https://github.com/stigrs/diimpy.git

### Building the Software

These steps assumes that the source code of this repository has been cloned
into a directory called `diimpy`.

The program is installed by executing:

        cd diimpy
        python -m pip install . --prefix=$HOME (%USERPROFILE% on Windows)

All tests should pass, indicating that your platform is fully supported: 

        python -m unittest ./tests/test_case.py
