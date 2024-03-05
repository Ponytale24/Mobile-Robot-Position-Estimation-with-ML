# Enhancing Mobile Robot Position Estimation with Machine Learning

Methods Using Camera-Based Tracking

The goal is to improve the position estimation of the mobile robot platform using ML. For this purpose, the position data of the Vicon camera system is used.

## Vicon Calibration / Alignment of measurement points

0. Remove any object from the measurement area (e.g. robot)
1. Reset with Calibration>Reset
2. Calibrate with WAND
3. Set Origin (with ActiveWand NOT v2)
4. Create Masks
5. Place Marker in the marked middle of the robot
6. Add marker to object (KMR_CENTER) and get Position of Marker1
7. set measurement point of the KMR_Platform Object to Marker1 location

## Rotation angle measurement

1. The robot drives 1 meter in a specific axis direction (x or y) within 35 seconds.
2. The robot stays still for 1 minute.
3. `calc_rotation_angle.py` cuts out the first 35 seconds and calculates the rotation angle for all subsequent samples, plots the results if desired, and writes the average angle to `alpha.txt`.

## Project Structure

- data
  - coords-rotation: csv files for calculating the alpha angle
  - recs: new recordings are stored here
  - rpi: csv files containing acceleration data from the Raspberry Pi Sense Hat module (high delay)
  - train: data used for training
  - valid: data used for validation
- models: contains model files to load to avoid retraining
- utils
  - `plots.py`: code for plotting
  - `preprocess_data.py`: code for loading dataframe and full dataset
  - `vicon_test.py`: a script for testing the vicon system
- `data_collector.py`: script used for collecting data from robot vicon and optionally raspberry pi
- `evaluation.ipynb`: notebook for evaluating data quality for a single trial (one csv-file)
- `evaluation_all.ipynb`: notebook for gathering average info about the data
- `lstm.ipynb`: notebook containing training and evaluation of the lstm model
- `xgboost.ipynb`: notebook containing training and evaluation of the xgboost model

## Nomenclature

General:

- Appendix V: Data from the Vicon Camera System
- Appendix R: Data from the Robot System
- Appendix P: Data from the Raspberry Pi

Timestamps:

All timestamps are recorded in the `data_collector.py` on the Recording PC

- tStart: Timestamp at the start of each sample
- tR: Timestamp right after Robot data was received
- tP: Timestamp right after Pi data was received
- tV: Timestamp right after Vicon data was received
