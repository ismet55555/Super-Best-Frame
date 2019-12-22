#!/usr/bin/env/python3

import sys
import os
import random
import cv2


print('===================')
print('Start')
print('')


# Image delay
image_delay = 3000

# Set up current directory path
currentDirectory = os.path.abspath(os.path.dirname(sys.argv[0])) 

# Path for images
imageDirectory  = "Images"
imageDirectory  = os.path.join(currentDirectory, imageDirectory) + "//"

# Array of opencv image objects
images = []
imageNames = []
imagePaths = []


# Loop through all images in the directory
for filename in os.listdir(imageDirectory):
    # Add image path
    imagePaths.append(imageDirectory + filename)
    # Add the name of the image to an array
    imageNames.append(filename)

# Opening openCV window
cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)
# Setting up openCV window for full screen mode
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#TODO: imshow a screen size blank image

try:
    while True:
        # Picking a random image form directory
        random.seed()
        imageIndex = random.randint(0, len(imagePaths)-1)

        print('Showing Image {} of {} ({})'.format(imageIndex, len(imagePaths), imageNames[imageIndex]))

        # Load the image
        imageFileObject = cv2.imread(imagePaths[imageIndex], cv2.IMREAD_UNCHANGED)

        # Showing/Updating Image
        cv2.imshow('Image', imageFileObject)
        
        # Waiting 2 seconds and watching out for key press to quit
        if cv2.waitKey(image_delay) == ord(' ') :
            break

except Exception as e:
    print(e)
    
finally:
    #Close all open openCV windows
    cv2.destroyAllWindows()

print('')
print('DONE!')
print('===================')
