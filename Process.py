import cv2

win = (500, 500)
r_big = 130
big = (((win[0]/2)-r_big, (win[1]/2)-r_big), ((win[0]/2)+r_big, (win[1]/2)+r_big)) # division between integers produces integer (by rounding)


def draw_square(im):
    ((xo, yo), (x, y)) = big
    cv2.line(im, (xo,yo), (x,yo), (0,255,0))
    cv2.line(im, (x,yo), (x,y), (0,255,0))
    cv2.line(im, (x,y), (xo,y), (0,255,0))
    cv2.line(im, (xo,y), (xo,yo), (0,255,0))


def region(im, margin):
    im[:big[0][0]-margin, :] = 0 #top
    im[:, :big[0][1]-margin] = 0 #left
    im[big[1][0]+margin:im.shape[1], :] = 0 #bottom
    im[:, big[1][1]+margin:im.shape[0]] = 0 #right


def show_intersections(im, intersections):
    for point in intersections:
        cv2.circle(im, (int(round(point[0])), int(round(point[1]))),
                   6, (0, 0, 255), -1)
    cv2.imshow("corners", im)


def preprocess(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # r, gray = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    # gray = cv2.erode(dst, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=5)

    return gray
