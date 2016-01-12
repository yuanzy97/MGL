# MGL
Processing of Department of Energy (DOE) data for Microgrid Labs

A variety of data processing tasks, mostly to do with processing CSV datasets from the Department of Energy (DOE). Each dataset tracks theenergy usage in several aspects from a particular type of institution in a particular place, e.g. 'hospital-JacksonMS' tracks the energy use in electricity, heating, etc. for a hospital in Jackson MS.

Dercam.py is prototypical for several of the data processing tasks. The goal of this particular program is to (i) Isolate a particular aspect of energy (e.g. all heating based on gas) and (ii) provide, for each month, a short list of representative profiles - weekday, weekend, and peak day. Some key features of the code:

(i) It is efficient, scaleable code that ensures that every csv row is read only once and that only short lists (for example, the profiles for a week) are stored in memory during execution of the code.

(ii) Outliers are statistically identified and accounted for 
