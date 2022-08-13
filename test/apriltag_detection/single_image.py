from picamera import PiCamera
import time
import cv2
import numpy as np
from dt_apriltags import Detector


visualization = True

originalimagepath = "tmp/orignal_img.jpg"
processedimagepath = "tmp/processed_img.jpg"
datapath = "tmp/data.txt"

at_detector = Detector(
    families="tag16h5",
    nthreads=1,
    quad_decimate=2.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0,
)

camera = PiCamera()
camera.rotation = 180

time.sleep(2)  # camera warm-up time

camera.capture(originalimagepath)

img = cv2.imread(originalimagepath, cv2.IMREAD_GRAYSCALE)

tags = at_detector.detect(img)
print(tags)

if visualization:
    cv2.imshow("Original image", img)

color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

f = open(datapath, "w")

for tag in tags:
    if tag.decision_margin > 20:
        f.write("tag_id:")
        f.write(str(tag.tag_id))
        f.write("\n")
        f.write("ceter:")
        f.write(str(tag.center[0]))
        f.write(",")
        f.write(str(tag.center[1]))
        f.write("\n")
        f.write("corners:")
        f.write("\n")
        for i in range(4):
            f.write(str(tag.corners[i, 0]))
            f.write(",")
            f.write(str(tag.corners[i, 1]))
            f.write("\n")
        f.write("homography:")
        f.write("\n")
        for i in range(3):
            for j in range(3):
                f.write(str(tag.homography[i, j]))
                f.write(",")
            f.write("\n")

        for idx in range(len(tag.corners)):
            cv2.line(
                color_img,
                tuple(tag.corners[idx - 1, :].astype(int)),
                tuple(tag.corners[idx, :].astype(int)),
                (0, 255, 0),
            )

        cv2.putText(
            color_img,
            str(tag.tag_id),
            org=(
                tag.corners[0, 0].astype(int) + 10,
                tag.corners[0, 1].astype(int) + 10,
            ),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,
            color=(0, 0, 255),
        )

if visualization:
    cv2.imshow("Detected tags", color_img)

    k = cv2.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv2.destroyAllWindows()
        
        
cv2.imwrite(processedimagepath,color_img)
