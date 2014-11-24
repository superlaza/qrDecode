import cv2
import numpy as np
from Process import draw_square, preprocess, region
from FindPoints import findPoints
from Transform import transform
import Errors

#the following are used to make calls to the system, and record the date of a qr decode
from subprocess import Popen, PIPE
import time

camera_port = 0
ramp_frames = 4

qr_out = "./qr_out.png"

win = (500, 500)

#debugging
suppress = True

#array keeps tracked of decoded student qrs
students = {}


def main():
    camera = cv2.VideoCapture(camera_port)
    success = False

    for i in xrange(ramp_frames):
        #first few reads from camera are duds, return values are tossed
        camera.read()

    while True:
        #The function waitKey waits for a key event infinitely (when delay<=0 )
        #or for delay milliseconds, when it is positive. It returns the code of
        #the pressed key or -1 if no key was pressed before the specified time
        #had elapsed. Escape code is 27
        wk = cv2.cv.WaitKey(10)
        if wk == 27:
            break

        if wk == 32 and cv2.getWindowProperty("success", cv2.CV_WINDOW_AUTOSIZE) > 0:
            cv2.destroyWindow("success")
            success = False

        retval, im = camera.read()

        try:
            #resize image to be a square
            im = np.array(im[:, :im.shape[0], :])
            im = cv2.resize(im, win)

            #present feed for input
            draw_square(im)
            cv2.imshow("Input", im)

            #resizes image, coverts to grayscale,
            #and produces the result of canny edge detection with a focus on a specific region
            gray = preprocess(im)

            edges = cv2.Canny(gray, 100, 240)
            region(edges, margin=0)  # section off ROI

            points = findPoints(edges)

            # for point in points:
            #     cv2.circle(im, tuple(point), 5, (0, 0, 0), -1)
            # cv2.imshow('intersections', im)

        except Errors.ImproperIntersectionsError as e:
            if not suppress:
                print e
            continue
        except Exception as e:
            if not suppress:
                print "Error in Preprocessing or Finding Intersections: ", e
            continue

        # show_intersections(im, intersections)

        try:
            # continue
            registered = transform(im, points)
        except Errors.NotEnoughPointsToTransformError as e:
            if not suppress:
                print e
            continue

        region(registered, margin=60)
        cv2.imshow("registered", registered)
        cv2.imwrite(qr_out, registered)

        p = Popen(['zbarimg', qr_out], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode

        if rc == 0 and (not success):
            cv2.imshow("success", cv2.imread('./check_mark.png'))
            success = True

            if output[8:] not in students:
                students.update({output[8:].strip("\r\n"): {"date": time.strftime("%d.%m.%y"), "time": time.strftime("%H:%M")}})

    cv2.cv.DestroyAllWindows()
    camera.release()

    print students
if __name__ == '__main__':
    main()
