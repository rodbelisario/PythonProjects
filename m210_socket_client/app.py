import cv2
import numpy as np
import socket
from struct import *
from collections import namedtuple


# global variables
# frame
img_width = 1280     # frame cols
img_height = 1024    # frame rows
img_elem_size = 3    # frame channels
img_data_size = img_width * img_height * img_elem_size   # frame totaldata
frame_info_size = 28
temetry_data_size = 0 #

def socket_connect():
    # connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _error = s.connect_ex(('localhost', 12000))
    if(_error == 0):
        print(f"s.fileno(): {s.fileno()}")
    else:
        print(f"Socket Connect Error: {_error}")
        exit(-1)
    return s

def receive_frame(s):
    buff = bytearray()
    while(len(buff) < img_data_size):
        packet = s.recv(1024)
        if packet:
            buff.extend(packet)
    
    bgr_image = np.array(buff).reshape(img_height, img_width, img_elem_size)
    
    return bgr_image

def receive_frame_info(s):
    buff = bytearray()
    while(len(buff) < frame_info_size):
        packet = s.recv(1024)
        if packet:
            buff.extend(packet)
    
    f_cols, f_rows, f_depth, f_type, f_total, f_channels, f_elemSize = unpack('iiiiiii', buff)

    print(f_cols)
    print(f_rows)
    print(f_depth)
    print(f_type)
    print(f_total)
    print(f_channels)
    print(f_elemSize)
    
    return

def receive_telemetry(s):
    buff = bytearray()
    telemetry_data_size = calcsize('BIIiiifddHfffIIIIIIIIIIIIIIIIIIfhhhfffff')
    while(len(buff) < telemetry_data_size):
        packet = s.recv(1024)
        if packet:
            buff.extend(packet)
    
    Drone_info = namedtuple('drone_info', 'statusFlight gpsDate gpsTime                 \
                            gpsPosition_x gpsPosition_y gpsPosition_z                   \
                            gpsFused_altitude gpsFused_latitude                         \
                            gpsFused_longitude gpsFused_visibleSatelliteNumber          \
                            gimbalAngles_x gimbalAngles_y gimbalAngles_z                \
                            gimbalStatus_calibrating gimbalStatus_disabled_mvo          \
                            gimbalStatus_droneDataRecv gimbalStatus_escPitchStatus      \
                            gimbalStatus_escRollStatus gimbalStatus_escYawStatus        \
                            gimbalStatus_FWUpdating gimbalStatus_gear_show_unable       \
                            gimbalStatus_gyroFalut gimbalStatus_initUnfinished          \
                            gimbalStatus_installedDirection gimbalStatus_isBusy         \
                            gimbalStatus_mountStatus gimbalStatus_pitchLimited          \
                            gimbalStatus_prevCalibrationgResult gimbalStatus_reserved2  \
                            gimbalStatus_rollLimited gimbalStatus_yawLimited            \
                            altitudeFusioned compass_x compass_y compass_z              \
                            altitudeBarometer quaternion_q0 quaternion_q1               \
                            quaternion_q2 quaternion_q3')

    try:
        drone_info = Drone_info._make(unpack('BIIiiifddHfffIIIIIIIIIIIIIIIIIIfhhhfffff', buff))
        print(drone_info)
    except:
        print("Exeption - unpack requires a buffer of 168 bytes")
        print(len(buff))

    

def main():
    print(f"SIZE OF TELEMETRY DATA: {calcsize('BIIiiifddHfffIIIIIIIIIIIIIIIIIIfhhhfffff')}")
    print("Please, check if the value SIZE OF TELEMETRY DATA on the cpp program is the same.")
    


    cv2.namedWindow('Python Window: Received Frame')

    img_socket = socket_connect()
    telemetry_socket = socket_connect()
    while(1):
        frame = receive_frame(img_socket)
        #receive_frame_info(telemetry_socket)
        receive_telemetry(telemetry_socket)
        cv2.imshow('Python Window: Received Frame',frame)
        if cv2.waitKey(20) & 0xFF == 27:
            break


if __name__ == '__main__':
    main()
