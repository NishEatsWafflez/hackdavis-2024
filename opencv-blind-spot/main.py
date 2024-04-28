import numpy as np
import cv2


hog = cv2.HOGDescriptor()
hog.setSVMDetector(
    cv2.HOGDescriptor_getDefaultPeopleDetector(),
)


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


h = HumanDetector(0)

while True:
    frame, status = h.detection()
    cv2.imshow("frame", frame)

    if not status:
        print("PERSON!!!")

    if cv2.waitKey(1) == ord('q'):
        break
