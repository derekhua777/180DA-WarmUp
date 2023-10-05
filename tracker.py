# camera
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
# thresholding
# https://stackoverflow.com/questions/26218280/thresholding-rgb-image-in-opencv
# contours and bounding box
# https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans
from collections import Counter

import warnings
warnings.filterwarnings("ignore")

cap = cv.VideoCapture(0)


def get_center_image(image):
    height, width, _ = image.shape
    center_x = width // 2
    center_y = height // 2

    # Calculate the coordinates of the top-left and bottom-right corners of the 100x100 region centered on the image
    top_left_x = center_x - 50  # 100/2
    top_left_y = center_y - 50  # 100/2
    bottom_right_x = center_x + 50  # 100/2
    bottom_right_y = center_y + 50  # 100/2

    # Extract the center 100x100 region from the original image
    return image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]


while(True):
    # Capture frame-by-frame
    ret, image = cap.read()

    # Our operations on the frame come here
    #image = cv.cvtColor(image, cv.COLOR_RGB2HSV)

    center_image = get_center_image(image)
    center_image = center_image.reshape((center_image.shape[0] * center_image.shape[1],3)) #represent as row*column,channel number

    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(center_image)

    dominant_colors = clt.cluster_centers_.astype(int)
    color_counts = Counter([tuple(color) for color in dominant_colors])
    main_color = color_counts.most_common(1)[0][0]
    main_color = list(main_color)

    print("Center Color:", main_color)
    
    thresh = cv.inRange(image, (127,127,127), (255,255,255))

    contours,hierarchy = cv.findContours(thresh, 1, 2)
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.intp(box)
        cv.drawContours(image,[box],0,(0,0,0),2)


    height, width, _ = image.shape
    center_x = width // 2
    center_y = height // 2

    # Calculate the coordinates of the top-left and bottom-right corners of the 100x100 region centered on the image
    top_left_x = center_x - 50  # 100/2
    top_left_y = center_y - 50  # 100/2
    bottom_right_x = center_x + 50  # 100/2
    bottom_right_y = center_y + 50  # 100/2
    cv.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)

    cv.imshow('frame', image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()