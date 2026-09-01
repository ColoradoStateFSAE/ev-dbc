# Ram Racing: EV CAN DBC

This repository contains the `.dbc` files for the following devices used on the EV subteam:
- Display (Ram Racing)
- Izze-Racing Inertial Measurement Unit
- Rinehart PM100 DX Motor Controller
- AiM XLOG Datalogger

The `.dbc` files are then generated into a C library using the python `cantools` utility.

## Adding a `DBC`:
1. Upload a `.dbc` to the `dbc/` folder
2. If data-logging is done by the AiM XLOG, make the respective changes to [aim-filtered-dbc.py](scripts/aim-filtered-dbc.py) to ensure that the 16 char name limit is followed.
3. Commit & Push to trigger a [workflow](.github/workflows/release.yml) run that will build the C library.