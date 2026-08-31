"""Standard vocabularies used alongside the Canadian FWI System in British Columbia.

`FuelType` is the CFFDRS fuel-type classification published by Natural Resources Canada.
`BECZone` is the Province of British Columbia's biogeoclimatic ecosystem classification.
Both are public standards, reproduced here so the FWI code can be used with B.C. data
without pulling in a heavier dependency.
"""

from __future__ import annotations

from enum import Enum


class FuelType(str, Enum):
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"
    C6 = "C6"
    C7 = "C7"
    D1 = "D1"
    D2 = "D2"
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"
    O1A = "O1A"
    O1B = "O1B"
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    NON_FUEL = "NF"
    WATER = "WA"


class BECZone(str, Enum):
    AT = "AT"
    BAFA = "BAFA"
    BG = "BG"
    BWBS = "BWBS"
    CDF = "CDF"
    CWH = "CWH"
    CMA = "CMA"
    ESSF = "ESSF"
    ICH = "ICH"
    IDF = "IDF"
    IMA = "IMA"
    MH = "MH"
    MS = "MS"
    PP = "PP"
    SBPS = "SBPS"
    SBS = "SBS"
    SWB = "SWB"


BEC_ZONE_NAMES = {
    "AT": "Alpine Tundra",
    "BAFA": "Boreal Altai Fescue Alpine",
    "BG": "Bunchgrass",
    "BWBS": "Boreal White and Black Spruce",
    "CDF": "Coastal Douglas-fir",
    "CWH": "Coastal Western Hemlock",
    "CMA": "Coastal Mountain-heather Alpine",
    "ESSF": "Engelmann Spruce-Subalpine Fir",
    "ICH": "Interior Cedar-Hemlock",
    "IDF": "Interior Douglas-fir",
    "IMA": "Interior Mountain-heather Alpine",
    "MH": "Mountain Hemlock",
    "MS": "Montane Spruce",
    "PP": "Ponderosa Pine",
    "SBPS": "Sub-Boreal Pine-Spruce",
    "SBS": "Sub-Boreal Spruce",
    "SWB": "Spruce-Willow-Birch",
}
