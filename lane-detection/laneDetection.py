from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import numpy as np
import cv2
import math
import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import serial
import numpy as np
import cv2
import sys
from random import randint

hog = cv2.HOGDescriptor()
hog.setSVMDetector(
    cv2.HOGDescriptor_getDefaultPeopleDetector(),
)
# roi_x = 50
# roi_y = 50
# roi_w = 50
# roi_h = 50

FACE_THRESHOLD = 50

class FaceDetector:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
    def detection(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))
            image, status = faceProcess(frame)
            print(status)
            return image, status
        return None, True
def faceProcess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, width = frame.shape[:2]
    roi_x = width//3
    roi_y = height//4
    roi_w = width//3
    roi_h = height//2
    

    # contours, _ = cv2.findContours(preprocess(frame), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    faces = face_cascade.detectMultiScale(frame, 1.3, 5, minSize=(40, 40))
    status = True

    if not any(map(len, faces)):
        print("Face has crossed the threshold!")
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Look Out!', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        status = False

    else:
        # Draw bounding boxes around the detected contours
        for (x,y,w,h) in faces:
            # x, y, w, h = cv2.boundingRect(face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Calculate the center of the face
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            # Calculate the center of the ROI
            roi_center_x = roi_x + roi_w // 2
            roi_center_y = roi_y + roi_h // 2

            # Calculate the distance between the face center and the ROI center
            distance = ((face_center_x - roi_center_x) ** 2 + (face_center_y - roi_center_y) ** 2) ** 0.5

            # Check if the face has passed the threshold
            if (distance > FACE_THRESHOLD):
                # Do something when the facea passes the threshold (e.g., print a message)
                print("Face has crossed the threshold!")
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'Look Out!', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
                status = False
                


                # These are causing errors (probably b/c we don't have anything connected).
                # ser = serial.Serial('/dev/ttyACM0', 9600)
                # ser.write(b'SIGNAL') 
                # ser.close()

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

              


    # Draw the ROI frame
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)
    return frame, True




class HumanDetector:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

    def process(self, frame, boxes):
        status = True

        if len(boxes) > 0:

            for box in boxes:

                w = box[2] - box[0]
                h = box[3] - box[1]

                if h > 250:
                    status = False

                    print(w, h)

        return frame, status

    def detection(self):
        ret, frame = self.cap.read()

        if ret:

            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            for xA, yA, xB, yB in boxes:
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

            # Human is TOO close - False

            # Human is safe distance - True

            frame, status = self.process(frame, boxes)

            return frame, status

        return None, False


class LaneDetectionModel:
    def __init__(self, videoSource):
        self.cap = cv2.VideoCapture(videoSource)

    def detection(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))
            image, status = processer(frame)
            print(status)
            return image, status
        return None, True

        #cv2.imshow("Processed Frame with Overlays", image)


class LaneDetector:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window_title = window_title
        self.button_frame = tk.Frame(window)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)
        #self.cap = cv2.VideoCapture(video_source)
        self.btn_switch_model = tk.Button(self.button_frame, text="Lane Detection", width=15, command=lambda: self.switch_model("Model 1"))
        self.btn2_switch_model = tk.Button(self.button_frame, text="Facial Tracking", width=15, command=lambda: self.switch_model("Model 2"))
        self.btn3_switch_model = tk.Button(self.button_frame, text="Blind Spot", width=15, command=lambda: self.switch_model("Model 3"))
        self.btn_switch_model.pack(side=tk.LEFT, expand=True)
        self.btn2_switch_model.pack(side=tk.LEFT, expand=True)
        self.btn3_switch_model.pack(side=tk.LEFT, expand=True)
        #self.btn_switch_model.grid(row=0, column=0)
        #self.btn2_switch_model.grid(row=0, column=1)
        #self.btn3_switch_model.grid(row=0, column=2)
        #btn = Button(window, text = 'Click me !', bd = '5',
       #                   command = self.switch_model)
        self.label = tk.Label(window)
        self.label.pack()

# Set the position of button on the top of window.
        #btn.pack(side = 'top')

        self.video_sources = {
                "Model 1": 0,
                "Model 2": 1,
                "Model 3": 2
                }
        self.current_model = "Model 1"
        model1 = LaneDetectionModel(self.video_sources["Model 1"])
        model2 = FaceDetector(self.video_sources["Model 2"])
        model3 = HumanDetector(self.video_sources["Model 3"])

        self.models = {
            "Model 1": model1,
            "Model 2": model2,
            "Model 3": model3
        }

        self.update()

        self.window.mainloop()

    def switch_model(self, model):
        print("THE NEW MODEL  SHOULD BE" + model)
        self.current_model = model

    def update(self):
        image1, status1 = self.models["Model 1"].detection()
        image2, status2 = self.models["Model 2"].detection()
        image3, status3 = self.models["Model 3"].detection()
        if not status1:
            self.current_model = "Model 1"
        elif not status2:
            self.current_model = "Model 2"
        elif not status3:
            self.current_model = "Model 3"
        if self.current_model == "Model 1":
            image = image1
        elif self.current_model == "Model 2":
            image = image2
        else:
            image = image3


        #cv2.imshow("Processed Frame with Overlays", image)
        if image is None:
            self.window.after(10, self.update)


        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image)
        except:
            print(image)
            pass
            # Convert the frame to a PIL Image
        #img = img.resize((self.label.winfo_width(), self.label.winfo_height()), Image.ANTIALIAS)

            # Convert the resized PIL Image to a Tkinter-compatible image
        # Convert the PIL Image to a Tkinter-compatible image
        imgtk = ImageTk.PhotoImage(image=img)
        # Display the image on the label
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.window.after(10, self.update)
def display_lines(image, lines):
    lines_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            try:
                x1, y1, x2, y2 = line
                cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            except:
                print("fail")
    return lines_image

def average(image, lines):
    left = []
    right = []

    if lines is not None:
      for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        if len(parameters) != 2:
            print("HELP")
        slope = parameters[0]
        y_int = parameters[1]
        if slope < 0:
            left.append((slope, y_int))
        else:
            right.append((slope, y_int))

    right_avg = np.average(right, axis=0)
    left_avg = np.average(left, axis=0)
    farLeft, farRight = False, False
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    try:
        farLeft = math.isnan(right_avg)
        #ser = serial.Serial('/dev/ttyACM0', 9600)
        #ser.write(b'LANE_LEFT_SIG')
        #ser.close()
    except:
        farLeft = False
    try:
        farRight = math.isnan(left_avg)
        #ser.write(b'LANE_RIGHT_SIG')
        #ser.close()
    except:
        farRight = False
    if farLeft or farRight:
        print(farRight)
        return np.array([])
    left_line = make_points(image, left_avg)
    right_line = make_points(image, right_avg)
    return np.array([left_line, right_line])

def make_points(image, average):
    slope, y_int = average
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - y_int) // slope)
    x2 = int((y2 - y_int) // slope)
    return np.array([x1, y1, x2, y2])


# Read the video from specified path


#plt.imshow(image)
#plt.show()
def processer(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #plt.imshow(grayImage, cmap = plt.cm.gray)
    #plt.show()

    grayImage = cv2.blur(grayImage, (5, 5))
    cannyImage = cv2.Canny(grayImage, 25, 75)
#plt.figure()
    #plt.imshow(cannyImage, cmap = plt.cm.gray)
    #plt.show()

    height, width = cannyImage.shape[:2]

    bottom_left = (0, height)  # Bottom left corner
    left_mid = (width//2, 2*height//3)  # Left mid
#right_mid = (width, height//2)  # Right mid
    bottom_right = (width, height)  # Bottom right corner

    mask = np.zeros_like(cannyImage)


    ignore_mask_color = 255
    bottom_left = [0, height]
    top_left	 = [width*.5, 4*height/8]
    bottom_right = [width, height]
#top_right = [width*.7, height * 0.65]
    vertices = np.array([[bottom_left, top_left, bottom_right]], dtype=np.int32)
# filling the polygon with white color and generating the final mask
    cv2.fillPoly(mask, vertices, ignore_mask_color)
# performing Bitwise AND on the input image and mask to get only the edges on the road
    masked_image = cv2.bitwise_and(cannyImage, mask)
    #return masked_image




#triangle = [bottom_left, left_mid, bottom_right]
#triangle = np.array([triangle], np.int32)
#cv2.fillPoly(mask, triangle, 255)

#masked_image = cv2.bitwise_and(cannyImage, mask)



    #plt.imshow(masked_image)
    #plt.show()
    lines = cv2.HoughLinesP(masked_image, rho=6, theta=np.pi/160, threshold=160, lines=np.array([]), minLineLength=40, maxLineGap=25)


    averaged_lines = average(image, lines)
    if len(averaged_lines)==2:
        print("testing")
        black_lines = display_lines(image, averaged_lines)
        lx1, lx2, ly1, ly2 = averaged_lines[0]
        leftSlope = (ly2-ly1)/(lx2-lx1)
        rx1, rx2, ry1, ry2 = averaged_lines[1]
        rightSlope = (ry2-ry1)/(rx2-rx1)

        print(leftSlope)
        print(rightSlope)
        print((rightSlope*-1)/leftSlope >= 1.25)
        print((rightSlope*-1)/leftSlope <= .8)

        center = ((leftSlope*lx1-rightSlope*rx2) - (ly1-ry2))//(leftSlope-rightSlope)
        print(center)

        lanes = cv2.addWeighted(image, 0.8, black_lines, 1, 1)
        return lanes, True
        #plt.imshow(lanes)
        #plt.show()
    else:
        image = cv2.putText(image, 'CAUTION: OUT OF LANE BOUNDS', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        print("THIS FAILED")
        return image, False
        #plt.imshow(image)


#averaged_liens[0] is left line, split into x1, y1, x2, y2




'''
cap = cv2.VideoCapture(1)

app = Tk()

# Bind the app with Escape keyboard to
# quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Create a label and display it on app
label_widget = Label(app)
label_widget.pack()

    # Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Unable to open webcam.")
    exit()

# Loop to capture and process each frame
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    #frame = mpimage.imread('roads.jpg')

    # Check if the frame was read successfully
    if not ret:
        print("Error: Unable to read frame.")
        break
    #cv2.imshow("Processed Frame with Overlays", frame)
    image = processer(frame)
    cv2.imshow("Processed Frame with Overlays", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


'''
root = tk.Tk()
# Set the window title
root.title("Webcam App")
# Create the WebcamApp object with the Tkinter window as its parent
app = LaneDetector(root, "Webcam App")

