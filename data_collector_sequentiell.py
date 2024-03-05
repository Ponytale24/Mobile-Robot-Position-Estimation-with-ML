from datetime import datetime
import socket
import time
import pandas as pd
from vicon_dssdk import ViconDataStream
import numpy as np

USE_RPI = False
USE_UDP = False
BUFFER_SIZE = 512
SLEEP_INTERVAL = 0.05

trial_name = input("What should the recording be named?: ")
current_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M')

# vicon client
client = ViconDataStream.Client()
client.Connect("localhost:801")

# Enable all the data types
client.GetFrame()
client.EnableSegmentData()
client.GetFrame()

subjectName = "Plattform_KMR"
segmentName = client.GetSegmentNames(subjectName)[0]

print("Vicon - Connected to localhost:801")

robot_server_address = ('10.200.87.30', 8000)
pi_server_address = ('10.200.87.30', 8002)

if USE_UDP:
    robot_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    robot_socket_udp.bind(robot_server_address)

    print(f"UDP Robot Server is listening on {robot_server_address}")

    # raspberry pi client
    if USE_RPI:
        pi_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pi_socket_udp.bind(pi_server_address)

        print(f"UDP Pi Server is listening on {pi_server_address}")
else:
    robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # robot_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    robot_socket.bind(robot_server_address)
    print("Waiting for robot to connect ...")
    robot_socket.listen()

    robot_connection, robot_address = robot_socket.accept()

    print(f"Robot TCP - Connected to: {robot_address[0]}:{robot_address[1]}")

    # raspberry pi client
    if USE_RPI:
        print("Waiting for pi to connect ...")
        pi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pi_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        pi_socket.bind(pi_server_address)
        pi_socket.listen()

        pi_connection, pi_address = pi_socket.accept()
        print(f"Pi TCP - Connected to: {pi_address[0]}:{pi_address[1]}")

data_list = []
saved = False
try:
    if not USE_UDP:
        start_msg = "Start\n"
        robot_connection.send(start_msg.encode())
        if USE_RPI:
            pi_connection.send(start_msg.encode())
        print("Started Recording")

    while True:
        tStart = time.time() 
        if USE_UDP:
            robot_data, robot_address = robot_socket_udp.recvfrom(BUFFER_SIZE)
            robot_data = robot_data.decode()
        else:
            robot_data = robot_connection.recv(BUFFER_SIZE).decode()

        tR = time.time()
        if robot_data == '' or robot_data == 'close':
            print("Robot closed connection")
            break

        if USE_RPI:
            if USE_UDP:
                pi_data, pi_address = pi_socket_udp.recvfrom(BUFFER_SIZE)
                pi_data = pi_data.decode()
            else:
                pi_data = pi_connection.recv(BUFFER_SIZE).decode()
            
            tP =time.time()
            if pi_data == '':
                print("RPi closed connection")
                break

        client.GetFrame()
        global_translation = client.GetSegmentGlobalTranslation(subjectName, segmentName)
        global_rotation = client.GetSegmentGlobalRotationEulerXYZ(subjectName, segmentName)
        tV = time.time()
        xV, yV, zRotV = global_translation[0][0], global_translation[0][1], global_rotation[0][2]
        
        # data processing
        xR, yR, theta, xR_fine, yR_fine = robot_data.split()

        if USE_RPI:
            # gyro is nan atm because its to slow to get accel and gyro 
            gxP, gyP, gzP, axP, ayP, azP = pi_data.split()
        else:
            tP, gxP, gyP, gzP, axP, ayP, azP = [np.NaN] * 7

        data_list.append({
            "tStart": tStart,

            "tR": tR,
            "xR": xR,
            "yR": yR,
            "theta": float(theta),
            "xR_fine" : xR_fine,
            "yR_fine" : yR_fine,

            "tV": tV,
            "xV": xV,
            "yV": yV,
            "zRotV": zRotV,

            "tP" : tP,
            "gxP": gxP,
            "gyP": gyP,
            "gzP": gzP,
            "axP": axP,
            "ayP": ayP,
            "azP": azP
            })

        time.sleep(SLEEP_INTERVAL) 
        
        confirm_msg = "Done\n"
        if USE_UDP:
            robot_socket_udp.sendto(confirm_msg.encode(), robot_address)
        else:
            robot_connection.send(confirm_msg.encode())
        if USE_RPI:
            if USE_UDP:
                pi_socket_udp.sendto(confirm_msg.encode(), pi_address)
            else:
                pi_connection.send(confirm_msg.encode())

    pd.DataFrame(data_list).to_csv(f"data/recs/{current_datetime}-{trial_name}.csv", index=False)
    saved = True

except KeyboardInterrupt:
    print("User ended Recording")
    pass

finally:
    print(f"Ended Recording, saved csv = {saved}")
    if USE_UDP:
        robot_socket_udp.close()
    else:
        robot_connection.close()
    if USE_RPI:
        if USE_UDP:
            pi_socket_udp.close()
        else:
            pi_connection.close()
    



