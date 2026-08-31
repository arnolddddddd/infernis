# INFERNIS — fire weather

**A tested implementation of the Canadian Forest Fire Weather Index System, from the engine
behind [Argon BI Systems](https://infernis.ca)' environmental risk platforms.**

This is the fire-weather core of INFERNIS: FFMC, DMC, DC, ISI, BUI and FWI, computed to the
standard CFFDRS equations, with the fuel-type and biogeoclimatic vocabularies needed to use them
with British Columbia data.

It is published so the arithmetic underneath our fire products can be checked by anyone, against
a standard that is itself public.

## Check it yourself

The test suite reproduces the worked example published with the standard — Van Wagner & Pickett
(1985), *Forestry Technical Report 33* — from the documented season-startup state:

| | FFMC | DMC | DC | ISI | BUI | FWI |
|---|---|---|---|---|---|---|
| reference | 87.7 | 8.5 | 19.0 | 10.9 | 8.5 | 10.1 |
| this code | 87.7 | 8.5 | 19.0 | 10.9 | 8.5 | 10.1 |

```bash
pip install -e ".[dev]"
pytest
```

```python
from infernis_fire.fwi import FWIService

FWIService().compute_daily(
    temp=17.0, rh=42.0, wind=25.0, precip=0.0, month=4,
    prev_ffmc=85.0, prev_dmc=6.0, prev_dc=15.0,
)
# {'ffmc': 87.7, 'dmc': 8.5, 'dc': 19.0, 'isi': 10.9, 'bui': 8.5, 'fwi': 10.1}
```

The codes are cumulative — FFMC, DMC and DC carry forward day to day. `compute_season` advances a
sequence of days for you; `compute_daily` expects you to pass yesterday's state.

## What is here, and what is not

**Here.** The Fire Weather Index System, and the CFFDRS fuel types and B.C. biogeoclimatic zones
as published standards.

**Not here.** The ignition model and its trained weights, its calibration, the danger-level cuts,
the feature pipeline, the data-acquisition stack, and everything for flood, smoke and property
assessment. Those are the parts of INFERNIS that are our own work rather than an implementation of
a public standard, and they are not open source.

We would rather be precise about that than let "open source" imply more than it covers. The FWI
System is a national standard published by Natural Resources Canada; implementing it correctly is
table stakes, not a differentiator. What this repository lets you verify is that we do implement it
correctly.

## Using the engine

The engine itself is free to use at **[ArSite.ca](https://arsite.ca)** — a province-wide wildfire
risk map that needs no account, a reading for any B.C. address with a free one, and a rate-limited
API key. Flood modelling, portfolio-scale property scoring and higher-volume API access are the
commercial product.

## On measurement

[`docs/SCORECARD.md`](docs/SCORECARD.md) records how the daily fire ranking performed against every
qualifying fire in a fixed window — including the ones it missed, and including the finding that on
that window it was **indistinguishable from a free static ignition map**. It is published because
"what did you say the day before?" is the first question anyone sensible asks, and the honest answer
includes the misses.

No claim of predictive skill over free public data is made anywhere in this repository. Where the
daily ranking is described, it is a **relative ranking**, never a calibrated probability of ignition.

## Sources

Built on open government and scientific data: Environment and Climate Change Canada, Natural
Resources Canada, the Province of British Columbia, NASA and Copernicus.

## Licence

Apache 2.0. See [LICENSE](LICENSE).

INFERNIS is the environmental risk engine built by Argon BI Systems Inc.
