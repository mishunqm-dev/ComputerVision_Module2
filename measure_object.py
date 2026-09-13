import cv2
import numpy as np
import os

# ---------------------------------------------------------
# CSC 8830 - Computer Vision
# Module 2 Assignment
# Step 2: Real-World 2D Object Measurement
# ---------------------------------------------------------

# Load the calibration results created in Step 1
calibration = np.load("calibration_data.npz")

camera_matrix = calibration["camera_matrix"]
distortion = calibration["distortion"]

fx = float(calibration["fx"])
fy = float(calibration["fy"])

image_width = int(calibration["image_width"])
image_height = int(calibration["image_height"])

print("\n--------------------------------------")
print("REAL-WORLD OBJECT MEASUREMENT")
print("--------------------------------------")

print("\nCamera calibration loaded successfully.")
print(f"fx = {fx:.4f}")
print(f"fy = {fy:.4f}")

# ---------------------------------------------------------
# GET TEST IMAGE
# ---------------------------------------------------------

image_name = input(
    "\nEnter the image filename from the test_images folder: "
).strip()

image_path = os.path.join(
    "test_images",
    image_name
)

image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(
        f"Could not open image: {image_path}"
    )

# ---------------------------------------------------------
# NORMALIZE IMAGE TO SAME ORIENTATION AND SIZE
# USED DURING CAMERA CALIBRATION
# ---------------------------------------------------------

height, width = image.shape[:2]

if width > height:
    image = cv2.rotate(
        image,
        cv2.ROTATE_90_CLOCKWISE
    )

image = cv2.resize(
    image,
    (image_width, image_height),
    interpolation=cv2.INTER_AREA
)

# ---------------------------------------------------------
# REMOVE CAMERA DISTORTION
# ---------------------------------------------------------

undistorted = cv2.undistort(
    image,
    camera_matrix,
    distortion
)

# ---------------------------------------------------------
# ENTER CAMERA-TO-OBJECT DISTANCE
# ---------------------------------------------------------

distance_m = float(
    input(
        "\nEnter camera-to-object distance in meters: "
    )
)

if distance_m <= 2.0:
    raise ValueError(
        "The assignment requires a distance greater than 2 meters."
    )

# ---------------------------------------------------------
# SELECT OBJECT IN IMAGE
# ---------------------------------------------------------

print("\nA new image window will open.")
print("Use the mouse to draw a tight rectangle around the object.")
print("Press ENTER or SPACE when finished.")

roi = cv2.selectROI(
    "Select Object",
    undistorted,
    showCrosshair=True,
    fromCenter=False
)

x, y, pixel_width, pixel_height = roi

cv2.destroyAllWindows()

if pixel_width == 0 or pixel_height == 0:
    raise RuntimeError(
        "No valid object was selected."
    )

# ---------------------------------------------------------
# PERSPECTIVE PROJECTION CALCULATION
# ---------------------------------------------------------
#
# Perspective projection:
#
# w = fx(W/Z)
# h = fy(H/Z)
#
# Solving for real-world dimensions:
#
# W = (w * Z) / fx
# H = (h * Z) / fy
#
# ---------------------------------------------------------

real_width_m = (
    pixel_width * distance_m
) / fx

real_height_m = (
    pixel_height * distance_m
) / fy

# Convert meters to centimeters
real_width_cm = real_width_m * 100
real_height_cm = real_height_m * 100

# Convert centimeters to inches
real_width_in = real_width_cm / 2.54
real_height_in = real_height_cm / 2.54

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

print("\n--------------------------------------")
print("MEASUREMENT RESULTS")
print("--------------------------------------")

print(f"\nPixel Width: {pixel_width} pixels")
print(f"Pixel Height: {pixel_height} pixels")

print(
    f"\nCamera-to-Object Distance: "
    f"{distance_m:.2f} meters"
)

print("\nEstimated Real-World Dimensions:")

print(
    f"Width: {real_width_cm:.2f} cm "
    f"({real_width_in:.2f} inches)"
)

print(
    f"Height: {real_height_cm:.2f} cm "
    f"({real_height_in:.2f} inches)"
)

print("\nPerspective Projection Equations:")

print("W = (w * Z) / fx")
print("H = (h * Z) / fy")