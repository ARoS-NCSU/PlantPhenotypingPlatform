# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import multiprocessing as mp
import numpy as np
import time
import cv2


def save_images(ev, q, finish):

    count = 0
    img = []

    while not finish.is_set() or (not q.empty):
        if ev.is_set():

            while q.empty():
                img.append(q.get())

            # Enters and exit Picture mode
            if count < 10:
                cv2.imwrite('phytotron_chamber_' + str(count) + '.png', img[count])
                count += 1
            else:
                img = []
                ev.clear()
                count = 0


if __name__ == '__main__':

    picture_res = (1920, 1080)
    video_res = (640, 480)
    frame_rate = 30

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = picture_res
    camera.framerate = frame_rate
    picture_resolution = picture_res
    rawCapture = PiRGBArray(camera, size=picture_res)
    # Used for annotating text to frames
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Wait camera to initialize
    time.sleep(0.1)
    picture_mode = False
    exit = False
    counter = 0
    pictures_set = 10
    increment = 0

    while True:
        if exit is True:
            break

        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            # Show the frame
            new_image = cv2.resize(image, video_res)

            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                exit = True
                break

            if counter == increment * pictures_set:
                picture_mode = False

            # Display recording mode
            if picture_mode:
                cv2.putText(new_image, 'Recording pictures ... ', (100, 500), font, 1, (255, 255, 255), 3, cv2.LINE_AA)
                cv2.imwrite('phytotron_chamber_' + str(counter) + '.png', image)
                counter += 1
            else:
                cv2.putText(new_image, 'Video Recording ... ', (100, 500), font, 1, (255, 255, 255), 3, cv2.LINE_AA)
                # Activate picture mode
                if key == ord("p"):
                    increment += 1
                    picture_mode = True

            cv2.imshow("Recording ... ", new_image)

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

        time.sleep(0.1)
