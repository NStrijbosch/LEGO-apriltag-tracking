from picamera import PiCamera
import time
import cv2


visualization = True

originalimagepath = "tmp/orignal_img.jpg"

camera = PiCamera()
camera.rotation = 180

time.sleep(2)  # camera warm-up time

camera.capture(originalimagepath)

img = cv2.imread(originalimagepath)

if visualization:
    cv2.imshow("Image", img)

    k = cv2.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv2.destroyAllWindows()
        
