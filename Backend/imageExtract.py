import cv2 as cv 
import numpy as np
from PIL import Image
from getNumberOfPins import getNumberOfPins

#rescales an image
def rescaleFrame(frame, scale=0.80):

    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def extractImages(screenshot):
    # Rescaling and cropping
    image = np.array(screenshot)
    
    # Convert RGB to BGR (OpenCV uses BGR by default)
    opencv_image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    resized_image = rescaleFrame(opencv_image, 0.50)
    cropped_image = resized_image[110:-20, 30:]

    cv.imshow('inital crop', cropped_image)

    # Retrieving the number of pins on the board
    num_pins = getNumberOfPins(cropped_image)

    # Converting to grayscale
    gray = cv.cvtColor(cropped_image, cv.COLOR_BGR2GRAY)

    # Blur, leaving edges intact
    blur = cv.medianBlur(gray, 11)
    #cv.imshow ('Blur', blur)

    # Use canny edge detection on blur
    canny = cv.Canny(blur, 40, 200)

    # Drawing canny results onto blank
    blank = np.zeros((canny.shape[0], canny.shape[1], 3), dtype='uint8')

    # Perform Contour detection on canny element
    contours, hierarchies = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Drawing contours onto blank
    blank_one = np.zeros((canny.shape[0], canny.shape[1], 3), dtype='uint8')
    cv.drawContours(blank_one, contours, contourIdx=-1, color=(0, 255, 0), thickness=1)

    # Approximate actual image edges (for when image edges bleed into image)
    bounding_rects = []
    for contour in contours:
        bounding_rects.append(cv.boundingRect(contour))

    # Storing rectangle areas and their corresponding indices
    areas = []
    index = 0
    for rectangle in bounding_rects:

        x, y, w, h = rectangle

        areas.append([w*h, index, x, y, w])

        index += 1

    # Sorting rectangle areas by size
    sorted_areas = sorted(areas, key=lambda x: x[0])

    # Storing only the num_pins amount of rectangles with the largest areas
    largest_rects = []
    for array in sorted_areas[-num_pins:]:
        largest_rects.append([array[1], array[2], array[3], array[4]])

    largest_rect_width = largest_rects[-1][3]

    sorted_indices = sorted(largest_rects, key=lambda point: (point[1]))

    empty_rect = []

    for array in sorted_indices:
        
        if largest_rect_width - array[3] < 10:
            empty_rect.append(array)

    # Drawing the num_pins amount of rectangles onto a prior image to check accuracy
    relative_index = 0
    real_rects = []

    for index in empty_rect:
    
        x, y, w, h = bounding_rects[index[0]]
        real_rects.append(bounding_rects[index[0]])

        cv.rectangle(gray, (x,y), (x + w, y + h), (0, 255, 0), 1)
        cv.putText(gray, f'{relative_index}', (x + 10, y -5), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
        relative_index += 1
        
    cropped_region_pil = []
    
    


    for rect in real_rects:
        x, y, w, h = rect  # Unpack bounding box coordinates
        cropped_region = cropped_image[y:y+h, x:x+w]  # Corrected cropping (y:y+h, x:x+w)
    
        cropped_region_pil.append(Image.fromarray(cropped_region))  # Convert to PIL image
        
    

    cv.rectangle

    cv.imshow('bounding rects', gray)

    cv.imshow('contours', blank_one)

    cv.imshow('blur webpage canny', canny)
    
    return(cropped_region_pil)

