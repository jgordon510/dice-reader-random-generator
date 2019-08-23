import cv2
min_threshold = 50                      # these values are used to filter our detector.
max_threshold = 200                     # they can be tweaked depending on the camera distance, camera angle, ...
min_area = 30                          # ... focus, brightness, etc.
min_circularity = .3
min_inertia_ratio = .5
def get_detector():
        params = cv2.SimpleBlobDetector_Params()                # declare filter parameters.
        params.filterByArea = True
        params.filterByCircularity = True
        params.filterByInertia = True
        params.minThreshold = min_threshold
        params.maxThreshold = max_threshold
        params.minArea = min_area
        params.minCircularity = min_circularity
        params.minInertiaRatio = min_inertia_ratio
     
        return cv2.SimpleBlobDetector_create(params)        # create a blob detector object.