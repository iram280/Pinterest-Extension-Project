import cv2 as cv 
import pytesseract
import numpy as np
import imageExtract

def iterative_sharpen(image, iterations=1):
    sharpened = image.copy()
    for _ in range(iterations):
        sharpened = cv.filter2D(sharpened, -1, np.array([[0, -1, 0],
                                                          [-1, 5, -1],
                                                          [0, -1, 0]]))
    return sharpened

def enhance_contrast(image, clip_limit=1.5, tile_grid_size=(4, 4)):
    lab = cv.cvtColor(image, cv.COLOR_BGR2LAB)
    l, a, b = cv.split(lab)
    
    # Apply CLAHE to the L channel
    clahe = cv.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l = clahe.apply(l)
    
    # Merge channels back and convert to BGR
    enhanced = cv.merge((l, a, b))
    return cv.cvtColor(enhanced, cv.COLOR_LAB2BGR)

# Returns number of pins on a pinterest board
def getNumberOfPins(image):

    # image processing for faster processing using pytesseract
    cropped_image = image[60:100, 450:500]

    scaled_crop = imageExtract.rescaleFrame(cropped_image, 4.5)

    scaled_crop = enhance_contrast(scaled_crop)
    cropped_rgb = cv.cvtColor(scaled_crop, cv.COLOR_BGR2RGB)
    black_and_white = cv.cvtColor(cropped_rgb, cv.COLOR_BGR2GRAY)
    black_and_white = iterative_sharpen(black_and_white)
    #black_and_white = cv.bilateralFilter(black_and_white, d=9, sigmaColor=75, sigmaSpace=75)
    #ret, thresh_photo = cv.threshold(black_and_white, 100, 255, cv.THRESH_BINARY)

    # Apply erosion
    #kernel = np.ones((3,3), np.uint8)  # Define the kernel size for erosion
    #eroded_img = cv.erode(thresh_photo, kernel, iterations=3)

    # Converting image text to a string, splitting, and returning only the number to convert to int
    try:
        num_pins = int(pytesseract.image_to_string(black_and_white).split()[0])
        print(num_pins)
    except:
        print("Couldn't find the number of pins")
        num_pins = 20

    cv.imshow('tesser pic', black_and_white)
    

    return num_pins
