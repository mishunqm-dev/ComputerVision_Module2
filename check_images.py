import cv2
import glob
import os

images = (
    glob.glob("calibration_images/*.jpg")
    + glob.glob("calibration_images/*.jpeg")
    + glob.glob("calibration_images/*.JPG")
    + glob.glob("calibration_images/*.JPEG")
)

print("\nCALIBRATION IMAGE SIZES\n")

for filename in images:
    image = cv2.imread(filename)

    if image is not None:
        height, width = image.shape[:2]

        print(
            os.path.basename(filename),
            "->",
            width,
            "x",
            height
        )