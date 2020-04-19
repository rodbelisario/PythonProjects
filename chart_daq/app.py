# @Author: Rodrigo Belisário Ramos
# @project_name: chart_daq
# 

import cv2
import numpy as np
import argparse
from  modules.chart import Chart

def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Chart-DAQ - Chart Data Acquisition")
    # -- Create the descriptions for the commands

    i_desc = "Image source path - Path of chart image that will be process"
    
    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # -- Create the arguments
    required.add_argument("-i", "--image", help=i_desc, required=True)
    args = vars(parser.parse_args())

    return args

def nothing(x):
    pass

def color_filter(img):
    
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.namedWindow("HSV-Filter", cv2.WINDOW_NORMAL)
    
    cv2.createTrackbar('Hue','HSV-Filter',127,255,nothing)
    cv2.createTrackbar('Saturation','HSV-Filter',127,255,nothing)
    cv2.createTrackbar('Value','HSV-Filter',127,255,nothing)
    cv2.createTrackbar('H-Range','HSV-Filter',255,255,nothing)
    cv2.createTrackbar('S-Range','HSV-Filter',255,255,nothing)
    cv2.createTrackbar('V-Range','HSV-Filter',255,255,nothing)

    while (1):

        hue = cv2.getTrackbarPos('Hue','HSV-Filter')
        saturation = cv2.getTrackbarPos('Saturation','HSV-Filter')
        value = cv2.getTrackbarPos('Value','HSV-Filter')
        h_range = cv2.getTrackbarPos('H-Range','HSV-Filter')
        s_range = cv2.getTrackbarPos('S-Range','HSV-Filter')
        v_range = cv2.getTrackbarPos('V-Range','HSV-Filter')

        h_min = hue - h_range
        s_min = saturation - s_range
        v_min = value - v_range
        h_max = hue + h_range
        s_max = saturation + s_range
        v_max = value + v_range
        
        print(f"{h_min}, {s_min}, {v_min}, {h_max}, {s_max}, {v_max}")

        lower_hsv = np.array([h_min, s_min, v_min])
        upper_hsv = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)
        img_filtered = cv2.bitwise_and(img, img, mask= mask)

        cv2.imshow('HSV-Filter', img_filtered)
        key = cv2.waitKey(1)
        if key == 27:
            break

    return img_filtered

def old_process(img):
    img_height, img_width, img_channels = img.shape
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for x in range(35,1150):
        pixels = []
        for y in range(0,img_height-1):
            if img_gray[y,x] > 0:
                pixels.append(y)
        if(len(pixels)>0):
            mean_y = int(np.mean(pixels))
            valor = (img_height - mean_y -38) / 1.48
            valor = round(valor, 2)
            print(f"x: {x}px, y: {mean_y}px -> valor: {valor}")
            img[mean_y, x] = (0,0,255)
            if x in [35, 112, 189, 266, 342, 418, 495, 571, 648, 724, 801, 878, 954, 1030, 1106, 1150]:
                cv2.putText(img, str(valor), (x, mean_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 1)
            cv2.imshow("img", img)
            cv2.waitKey(0)


def main():
    # get image path
    args = get_args()
    # get chart's axis using mouse 
    img_src = cv2.imread(args["image"])
    img_copy = img_src.copy()
    print(img_copy.shape)
    
    #chart = Chart(img_copy)
    '''
    x_min, x_max, y_min, y_max = get_chart_axis(img_copy)
    print(f"{x_min}, {x_max}, {y_min}, {y_max}")
    # color filter
    img_filtered = color_filter(img_copy)
    #process_chart
    old_process (img_filtered)
    return
    '''

if __name__ == '__main__':
    main()
