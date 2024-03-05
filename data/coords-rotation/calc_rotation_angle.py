import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

PLOT = False

def find_rotation_angle(point_original, point_target):
    # Calculate the dot product of the two vectors
    dot_product = np.dot(point_original, point_target)
    
    # Calculate the magnitudes of the vectors
    magnitude_original = np.linalg.norm(point_original)
    magnitude_target = np.linalg.norm(point_target)
    
    assert magnitude_original != 0, "magnitude original is 0, would cause zero division"
    assert magnitude_target != 0, "magnitude target is 0, would cause zero division"
    # Calculate the cosine of the angle between the vectors
    cos_theta = dot_product / (magnitude_original * magnitude_target)
    
    # Use the arccosine function to find the angle in radians
    angle_radians = np.arccos(cos_theta)
    
    # Convert radians to degrees
    angle_degrees = np.degrees(angle_radians)
    
    return angle_degrees

csv_files = [file for file in os.listdir("data/coords-rotation") if file.endswith('.csv')]
alphas = []



for idx, csv in enumerate(csv_files):
    sns.set_style("darkgrid")
    plt.figure(figsize=(20, 6))  # Set the figure size

    df = pd.read_csv("data/coords-rotation/" + csv)

    # converting time from ms to s
    df['tV'] = df["tV"] * 1000
    # unix to datetime
    df['tR_datetime'] = pd.to_datetime(df['tR'], unit="ms")
    df['tV_datetime'] = pd.to_datetime(df['tV'], unit="ms")

        # robot coords to mm
    df[["xR","yR"]] = df[["xR","yR"]] * 1000

    # zeroing initial position
    xR_0 = df["xR"][0]
    df["xR"] = df["xR"] - xR_0

    yR_0 = df["yR"][0]
    df["yR"] = df["yR"] - yR_0

    xV_0 = df["xV"][0]
    df["xV"] = df["xV"] - xV_0

    yV_0 = df["yV"][0]
    df["yV"] = df["yV"] - yV_0

    all_angles = []
    time = []
    # Create a Timedelta of 10 seconds
    time_duration = pd.Timedelta(seconds=35)
    # Calculate the new index based on the 'timestamp' column
    first_timestamp = df['tV_datetime'].iloc[0]
    new_index = first_timestamp + time_duration

    # If you want to find the index that is closest to the calculated new index
    closest_index = df['tV_datetime'].sub(new_index).abs().idxmin()


    for i in range(closest_index,len(df)):
        P1_R = (df["xR"][i],df["yR"][i])
        P1_V = (df["xV"][i],df["yV"][i])

        try:
            all_angles.append(find_rotation_angle(P1_R,P1_V))
            time.append(df["tV_datetime"][i])
        except AssertionError:
            pass

    print(f"{csv}: Mean Alpha: {round(np.mean(all_angles),3)}°, Std: {round(np.std(all_angles),5)}°")
    alphas.append(np.mean(all_angles))
    
    if PLOT:
        plt.scatter(time,all_angles, marker="x")
        plt.hlines(np.mean(all_angles), xmin=time[0], xmax=time[-1], colors="red", linestyles="dashed", alpha=0.6)
        plt.xlabel("Time")
        plt.ylabel("Angle (°)")
        plt.show()

print(f"Mean Alpha over all: {np.mean(alphas)}°")
print(f"Std Alpha over all: {np.std(alphas)}°")


# Open a file in write mode and save the float value as a string
with open('data/coords-rotation/alpha.txt', 'w') as file:
    file.write(str(np.mean(alphas)))


# 1.4353738114734225