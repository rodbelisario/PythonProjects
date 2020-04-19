import cv2
import numpy as np

class Axis:
    
    def onMouse(self, event, x, y, flags, param):
        points = param[0]
        window_name = param[1]
        img = param[2]

        if event == cv2.EVENT_LBUTTONDOWN:
            self._last_x = x
            self._last_y = y
            pass

        elif event == cv2.EVENT_LBUTTONUP:
            if self._last_x == x and self._last_y == y:
                points.append((x, y))
                print(x, y)
                img = cv2.circle(img, (x, y), 3, (0, 255, 0), 1)
                cv2.imshow(window_name, img)
                pass
            pass

    def __init__(self, img, axis_type="X/Y", min=0, max=0, marks=[], marks_gap=0):
        self._last_x = 0
        self._last_y = 0
        
        self.img = img
        self.min = min
        self.max = max
        self.marks = marks
        self.marks_gap = marks_gap
        self.axis_type = axis_type

        points = []
        window_name = "Axis " + self.axis_type + " Selection"

        param = []
        param.append(points)
        param.append(window_name)
        param.append(img)

        print(f"Select from the origin until the end of the Axis {axis_type}")
        print("the origin, every mark and the end of the axis")
        print("Press any key when finish selecting")

        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.onMouse, param)
        cv2.imshow(window_name, img)
        cv2.waitKey(0)

        x, y = zip(*points)

        if self.axis_type is "X":
            x = sorted(x)
            self.min = x[0]
            self.max = x[-1]
            self.marks = x[1:-1]
            self.marks_gap = np.mean(np.diff(self.marks))
        elif self.axis_type is "Y":
            # y = sorted(y, key=len, reverse=True) Problemas aqui -> y em ordem de menor para maior
            self.min = y[0]
            self.max = y[-1]
            self.marks = y[1:-1]
            self.marks_gap = np.mean(np.diff(self.marks))
        else:
            print("Axis_type should be X or Y")
            print(f"Got: {self.axis_type}")
            exit(-1)

        print(f"[DEBUG] Chart {self.axis_type}: ")
        print(f"[DEBUG] min: {self.min}")
        print(f"[DEBUG] max: {self.max}")
        print(f"[DEBUG] marks: {self.marks}")
        print(f"[DEBUG] marks_gap: {self.marks_gap}")

        pass
    pass


class Chart:
    def __init__(self, img):
        self.axis_x = Axis(img, "X")
        self.axis_y = Axis(img, "Y")
        pass

    pass


'''
NOW:

[DEBUG] Chart X: 
[DEBUG] min: 37
[DEBUG] max: 1161
[DEBUG] marks: [47, 114, 190, 265, 343, 420, 496, 574, 649, 725, 802, 879, 954, 1031, 1107]
[DEBUG] marks_gap: 75.71428571428571

[DEBUG] Chart Y: 
[DEBUG] min: 194
[DEBUG] max: 74
[DEBUG] marks: (165, 134, 105)
[DEBUG] marks_gap: -30.0
'''