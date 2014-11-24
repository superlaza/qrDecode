import cv2
import numpy as np
import Errors

#output image dimensions
myDims = [500, 500]


def transform(im, points):
    #a point list to indicate where the points found should be mapped to
    #list is sorted lexicographically
    p_list = [[50, 50], [450, 50], [50, 450], [450, 450]]

    #error if points are float32
    dst_square = np.array(p_list, np.float32)
    src_square = np.array(points,np.float32)
    
    if not (len(dst_square) - len(src_square)) == 0:
        raise Errors.NotEnoughPointsToTransformError
    
    #compute transform based on point mappings above
    _transform = cv2.getPerspectiveTransform(src_square, dst_square)

    registered = cv2.warpPerspective(im, _transform, tuple(myDims))

    return registered
