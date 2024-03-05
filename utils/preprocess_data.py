from numpy import radians, sin, array, cos
from pandas import to_datetime, read_csv
import os
import pandas as pd

def load_df(file_path):
    df = read_csv(file_path)
    # converting time from s to ms
    df['tStart'] = df['tStart'] * 1000
    df['tR'] = df['tR'] * 1000
    df['tP'] = df["tP"] * 1000
    df['tV'] = df["tV"] * 1000

    # unix to datetime
    df['tStart_datetime'] = to_datetime(df['tStart'], unit="ms")
    df['tR_datetime'] = to_datetime(df['tR'], unit="ms")
    df['tV_datetime'] = to_datetime(df['tV'], unit="ms")
    df['tP_datetime'] = to_datetime(df['tP'], unit="ms")


    order = ['tStart', 'tStart_datetime','tR', 'tR_datetime', 'xR', 'yR', 'theta', 'xR_fine','yR_fine', 'tV','tV_datetime', 'xV', 'yV', 'zRotV', 'tP', 'tP_datetime','axP', 'ayP', 'azP', 'gxP', 'gyP', 'gzP']
    df = df[order]

    # robot coords to mm
    df[["xR","yR"]] = df[["xR","yR"]] * 1000
    df[["xR_fine","yR_fine"]] = df[["xR_fine","yR_fine"]] * 1000

    # zeroing initial position
    xR_0 = df["xR"][0]
    df["xR"] = df["xR"] - xR_0

    yR_0 = df["yR"][0]
    df["yR"] = df["yR"] - yR_0

    xV_0 = df["xV"][0]
    df["xV"] = df["xV"] - xV_0

    yV_0 = df["yV"][0]
    df["yV"] = df["yV"] - yV_0


    # rotating coord systems
    with open('data/coords-rotation/alpha.txt', 'r') as file:
        alpha = radians(float(file.read()))

    c, s = cos(alpha), sin(alpha)
    R = array(((c, -s), (s, c)))

    # Create a NumPy array from the 'xV' and 'yV' columns
    xy_values = df[['xV', 'yV']].values

    # Use matrix multiplication to calculate the new values
    new_xy_values = R.dot(xy_values.T).T

    # Assign the new values back to the DataFrame
    df[['xV', 'yV']] = new_xy_values

    return df

def load_dataset(split):
    """_summary_

    Args:
        split (string): Load the "train" or "valid" or "rpi" data.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    if split == "train":
        dfs = []
        for i, csv in enumerate(os.scandir("data/train")):
            df = load_df(csv)
            df["trial_num"] = i
            df["timepoint"] = df.index
            df.set_index(['trial_num', 'timepoint'], inplace=True)
            dfs.append(df)
        return pd.concat(dfs, axis=0)
    if split == "valid":
        dfs = []
        for i, csv in enumerate(os.scandir("data/valid/")):
            df = load_df(csv)
            df["trial_num"] = i
            df["timepoint"] = df.index
            df.set_index(['trial_num', 'timepoint'], inplace=True)
            dfs.append(df)
        return pd.concat(dfs, axis=0)
    if split == "rpi":
        dfs = []
        for i, csv in enumerate(os.scandir("data/rpi/")):
            df = load_df(csv)
            df["trial_num"] = i
            df["timepoint"] = df.index
            df.set_index(['trial_num', 'timepoint'], inplace=True)
            dfs.append(df)
        return pd.concat(dfs, axis=0)
    else:
        raise Exception("Split must be either 'train' or 'valid' or 'rpi'")
    




