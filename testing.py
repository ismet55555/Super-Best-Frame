
import os
import cv2
import sys

import threading

thread_started = False


def thread():
    global thread_started
    print(thread_started)

    # Making a new window and setting its properties
    cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Loading the image
    currentDirectory = os.path.abspath(os.path.dirname(sys.argv[0]))
    imagepath = os.path.join(currentDirectory, 'Images/DSC02055.JPG')
    print(imagepath)
    img = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)

    # Showing the image
    while True:
        cv2.imshow('Image', img)
        if cv2.waitKey(0) == ord('q'):
            # Closing and exciting with "q"
            break

    # Closing all open OpenCV windows
    cv2.destroyAllWindows()

    thread_started = False





loops = 1
while True:

    if not thread_started:
        print('Starting Thread')
        thread = threading.Thread(target=thread)
        thread_started = True
        thread.start()


        # End after 3 times
        loops += 1
        if loops > 3:
            break
