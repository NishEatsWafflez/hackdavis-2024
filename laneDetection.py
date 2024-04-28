import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import numpy as np
import cv2
import math
import os 


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
    try:
        farLeft = math.isnan(right_avg)
    except:
        farLeft = False
    try:
        farRight = math.isnan(left_avg)
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

    grayImage = cv2.GaussianBlur(grayImage, (5, 5), 0)
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
        lanes = cv2.circle(lanes, (int(center), height//2), 5, (0, 0, 255), -1)
        return lanes
        #plt.imshow(lanes)
        #plt.show()
    else:
        image = cv2.putText(image, 'NO LANE DETECTED', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        return image
        #plt.imshow(image)


#averaged_liens[0] is left line, split into x1, y1, x2, y2




cap = cv2.VideoCapture(1)

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




