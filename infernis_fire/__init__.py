"""A tested implementation of the Canadian Forest Fire Weather Index System.

  fwi     FFMC, DMC, DC, ISI, BUI and FWI, computed to the standard CFFDRS equations
          and checked against the worked example in Van Wagner & Pickett (1985)

  enums   the CFFDRS fuel-type classification and British Columbia's biogeoclimatic
          zones — public standards, included so the FWI code is usable with B.C. data

This package is the fire-weather core of the INFERNIS engine. It is not the whole
engine: the ignition model, its calibration, the danger-level cuts and the data
pipeline are not published here. See README.md.
"""

__all__ = ["enums", "fwi"]
