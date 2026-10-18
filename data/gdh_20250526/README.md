# GDH and solar-wind data for 26 May 2025

This directory contains local input data for comparing the AMPS prediction with magnetic observations from Qeqertarsuaq (Godhavn, IAGA code `GDH`). The student notebook does not need network access.

## Files

- `gdh_magnetic_residual_20250526_1min.csv`: one-minute GDH measurements from VirES collection `SW_OPER_AUX_OBSM2_:GDH`, after subtraction of `CHAOS-Core + CHAOS-Static` by VirES.
- `swipe_drivers_20250526_1min.csv`: one-minute propagated OMNI solar-wind data, dipole tilt, F10.7, and the quasi-dipole coordinates and magnetic local time of GDH.
For GDH, the horizontal direction is obtained from IGRF-14 at the station: (\Delta H=\Delta B_N\cos D+\Delta B_E\sin D), where (D) is the IGRF declination. AMPS supplies the corresponding quasi-dipole northward ground perturbation. The daily median is removed from each time series to emphasize variations during the day rather than uncertain background offsets.

The comparison and figure are generated directly in `notebooks/04_ionospheric_electrodynamics.ipynb`. The source data can be reproduced with `scripts/download_gdh_amps_inputs.py`; students do not need to run that download script.

Sources: [VirES](https://vires.services/), [NASA CDAWeb HAPI](https://cdaweb.gsfc.nasa.gov/hapi), and [OMNI documentation](https://omniweb.gsfc.nasa.gov/html/ow_data.html). The AUX_OBS data are supplied by INTERMAGNET and remain subject to the [INTERMAGNET data conditions](https://intermagnet.org/data_conditions.html).
