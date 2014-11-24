import cv2
import numpy as np
import Errors
import random as r
from Process import show_intersections


def validatePoly(edges, polygon):
    #must be comprised of 4 points
    if len(polygon) == 4:
        #polygon is a stupidly nested structure, each point will be numpy array
        points = [p for [p] in polygon]

        #compute center
        center = np.round(sum(points)/4).astype(int)

        #we have our quad if its center is inside a radius of midpage
        r = 40
        offset = np.array([r, r])
        imcenter = np.array(list(edges.shape[::-1]))/2
        if all(center > imcenter-offset) and all(center < imcenter+offset):
            #sort points into TL, TR, BL, BR
            points = sorted([p for p in points if p[1] < center[1]], key = lambda (px,py): px)+\
                     sorted([p for p in points if p[1] > center[1]], key = lambda (px,py): px)
            return points

    return []


def findPoints(edges):
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #for every contour found, approximate it with a polygon and filter for
    #the desired quadrilateral
    for cnt in contours:
        polygon = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
        points = validatePoly(edges, polygon)

        color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        cv2.drawContours(edges, contours, contours.index(cnt), color, thickness=2)

        if points:
            return points
            
    #if you get through the whole list of contours without finding our quad,
    #throw an exception so the loop runs anew
    raise Errors.ImproperIntersectionsError
