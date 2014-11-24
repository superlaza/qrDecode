import cv2
# import numpy as np
from Process import draw_input_region, show_intersections, preprocess, postprocess
from FindPoints import findPoints
from Transform import transform
# from Grade import grade,ndrawAnswerCoords
import Errors

#the following are used to make calls to the system, and record the date of a qr decode
from subprocess import Popen, PIPE
import time

camera_port = 0
ramp_frames = 4

#for debugging
'''opts: output, processed, blend, region'''
view = ""
suppress = True

#array keeps tracked of decoded student qrs
students = {}

def main():
    #for criterion, minval can be any exorbitantly large value
    minval = 500000000
    quota = 0
    
    camera = cv2.VideoCapture(camera_port)

    for i in xrange(ramp_frames):
        #first few reads from camera are duds, return values are tossed
        retval, temp = camera.read()
    thresh = 0#testing
    while True:
        #The function waitKey waits for a key event infinitely (when delay<=0 )
        #or for delay milliseconds, when it is positive. It returns the code of
        #the pressed key or -1 if no key was pressed before the specified time
        #had elapsed. Escape code is 27
        wk = cv2.cv.WaitKey(10)


        # #testing
        # if wk == 2490368:
        #     thresh += 5
        # if wk == 2621440:
        #     thresh -= 5
        # print thresh

        if wk == 32:
            break
        #registration criterion, only grade if we've improved 7 times
        #break on space bar
        # if quota == 6 or wk == 32:
        #     #if registered exists, try grading it. otherwise, break
        #     #if reg exists and you grade it successfully, break. o/w keep going
        #     if 'registered' in locals():
        #         try:
        #             if not grade(registered):
        #                 cv2.imwrite('misaligned.jpg', blend_visual)
        #             break
        #         except:
        #             if not suppress:
        #                 print "something bad is happening at Grade"
        #     else:
        #         break
        
        retval, im = camera.read()

        try:
            #resizes image, coverts to grayscale,
            #and produces the result of canny edge detection with a focus on a specific region
            edges, gray = preprocess(im)

            #testing
            #cv2.imshow("edges", edges)

            cv2.imshow("Input", draw_input_region(im))

            # intersections = findPoints(gray)
            intersections = findPoints(edges)
            
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
            registered = transform(gray, intersections)
        except Errors.NotEnoughPointsToTransformError as e:
            if not suppress:
                print e
            continue
        
        cv2.imshow("registered", postprocess(registered))
        #cv2.imshow("registered", registered)
        cv2.imwrite("./test.jpg", postprocess(registered))

        p = Popen(['zbarimg', 'test.jpg'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode

        if rc == 0:
            # cv2.imshow("success", cv2.imread('./check_mark.png'))
            # cv2.destroyWindow("success")
            if output[8:] not in students:
                students.update({output[8:].strip("\r\n"): {"date": time.strftime("%d.%m.%y"), "time": time.strftime("%H:%M")}})
            continue

        print output, err

    cv2.cv.DestroyAllWindows()
    camera.release()


    print students
if __name__ == '__main__':
    main()
