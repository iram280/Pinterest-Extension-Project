import cv2 as cv 
import pytesseract
import numpy as np

# Returns number of pins on a pinterest board
def getNumberOfPins(image):

    # image processing for faster processing using pytesseract
    cropped_image = image[:15, :50]
    cropped_rgb = cv.cvtColor(cropped_image, cv.COLOR_BGR2RGB)
    black_and_white = cv.cvtColor(cropped_rgb, cv.COLOR_BGR2GRAY)
    #ret, thresh_photo = cv.threshold(black_and_white, 187, 255, cv.THRESH_BINARY)

    # Apply erosion
    #kernel = np.ones((3,3), np.uint8)  # Define the kernel size for erosion
    #eroded_img = cv.erode(thresh_photo, kernel, iterations=3)

    # Converting image text to a string, splitting, and returning only the number to convert to int
    try:
        num_pins = int(pytesseract.image_to_string(black_and_white).split()[0])
    except:
        print("Couldn't find the number of pins")
        num_pins = 12

    cv.imshow('tesser pic', black_and_white)

    return num_pins
