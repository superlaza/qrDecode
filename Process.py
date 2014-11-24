import cv2
import numpy as np

win = (500, 500)
#radius from center of image
r_big = 130
#division between integers produces integer (by rounding)
big = (((win[0]/2)-r_big, (win[1]/2)-r_big), ((win[0]/2)+r_big, (win[1]/2)+r_big))
small = ((150, 150), (350, 350))


def draw_square(im, ((xo, yo), (x, y))):
    cv2.line(im, (xo,yo), (x,yo), (0,255,0))
    cv2.line(im, (x,yo), (x,y), (0,255,0))
    cv2.line(im, (x,y), (xo,y), (0,255,0))
    cv2.line(im, (xo,y), (xo,yo), (0,255,0))


def draw_input_region(im):
    im = np.array(im[:,:im.shape[0],:])
    im = cv2.resize(im, win)

    draw_square(im, big)
    draw_square(im, small)

    return im


def region(im):
    im[:big[0][0],:] = 0 #top
    im[:,:big[0][1]] = 0 #left
    im[big[1][0]:im.shape[1],:] = 0 #bottom
    im[:,big[1][1]:im.shape[0]] = 0 #right
    im[small[0][0]:small[1][0],small[0][1]:small[1][1]] = 0 #inside


def show_intersections(im, intersections):
    for point in intersections:
        cv2.circle(im, (int(round(point[0])), int(round(point[1]))),
                   6, (0, 0, 255), -1)
    cv2.imshow("Corners", draw_input_region(im))


def preprocess(im):
    #resize image to be a square
    im = np.array(im[:, :im.shape[0], :])
    im = cv2.resize(im, win)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    #testing
    # postprocess(gray)
    # r, dst = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    # gray = cv2.erode(dst, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=5)
    # #cv2.imshow("thresh", dst)
    # edges = cv2.Canny(gray, 254, 255)
    # cv2.imshow('gray', gray)
    # cv2.imshow('gray', edges)

    edges = cv2.Canny(gray, 100, 240)
    region(edges)

    return edges, gray


#cut according to window specs,
#expand window to add a margin for error
def postprocess(im):
    margin = 60
    im[:big[0][0]-margin, :] = 0 #top
    im[:, :big[0][1]-margin] = 0 #left
    im[big[1][0]+margin:im.shape[1], :] = 0 #bottom
    im[:, big[1][1]+margin:im.shape[0]] = 0 #right

    return im