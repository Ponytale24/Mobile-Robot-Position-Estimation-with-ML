from matplotlib import pyplot as plt
import pandas as pd
from vicon_dssdk import ViconDataStream
import time

client = ViconDataStream.Client()
client.Connect("localhost:801")

#Enable all the data types
client.EnableMarkerData()
time.sleep(1)
client.GetFrame()
subjectName = "KMR_CENTER"

print("Vicon - Connected to localhost:801")


try:
    i = 1
    data_list = []
    while True:
            
        client.GetFrame()
        global_translation = client.GetMarkerGlobalTranslation(subjectName=subjectName, markerName="KMR_CENTER1")
        # x und y gedreht, daher erst 1 und dann 0 --- soll durch Rotatation ausgeglichen werden! 
        nV, tV, xV, yV, zV = i, time.time(), global_translation[0][0], global_translation[0][1], global_translation[0][2]
        print(f"xV: {xV}, yV: {yV}, zV: {zV}")
        i += 1
        data_list.append({
            "nV": nV,
            "tV": tV,
            "xV": xV,
            "yV": yV,
            "zV": zV
        })

except KeyboardInterrupt:
    df = pd.DataFrame(data_list)
    df["tV"] = pd.to_datetime(df["tV"], unit="s")
    # df.plot(x="tV", y="xV")
    #df.plot(x="tV", y="yV")
    plt.show()
    print(df[["xV","yV","zV"]].mean())
