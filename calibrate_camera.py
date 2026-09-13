import cv2
import numpy as np
import glob
import os

# ---------------------------------------------------------
# CSC 8830 - Computer Vision
# Module 2 Assignment
# Smartphone Camera Calibration
# ---------------------------------------------------------

# Printed checkerboard:
# 10 x 7 squares = 9 x 6 INTERNAL corners
CHECKERBOARD = (9, 6)

# Each square is 20 mm = 0.020 meters
SQUARE_SIZE = 0.020

# Normalize all calibration photos to the same size
TARGET_WIDTH = 1008
TARGET_HEIGHT = 1344

# Corner refinement criteria
criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

# ---------------------------------------------------------
# CREATE REAL-WORLD CHECKERBOARD COORDINATES
# ---------------------------------------------------------

object_pattern = np.zeros(
    (CHECKERBOARD[0] * CHECKERBOARD[1], 3),
    np.float32
)

object_pattern[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

# Scale coordinates using the real square size
object_pattern *= SQUARE_SIZE

object_points = []
image_points = []

# ---------------------------------------------------------
# LOAD ALL JPEG CALIBRATION IMAGES
# ---------------------------------------------------------

image_files = (
    glob.glob("calibration_images/*.jpg")
    + glob.glob("calibration_images/*.jpeg")
    + glob.glob("calibration_images/*.JPG")
    + glob.glob("calibration_images/*.JPEG")
)

print("\n--------------------------------------")
print("SMARTPHONE CAMERA CALIBRATION")
print("--------------------------------------")

print(f"\nFound {len(image_files)} calibration images.")

successful_images = 0
failed_images = 0

# ---------------------------------------------------------
# PROCESS EACH CALIBRATION IMAGE
# ---------------------------------------------------------

for filename in image_files:

    image = cv2.imread(filename)

    if image is None:
        print(f"COULD NOT READ: {filename}")
        continue

    height, width = image.shape[:2]

    # Rotate landscape images so all images use portrait orientation
    if width > height:
        image = cv2.rotate(
            image,
            cv2.ROTATE_90_CLOCKWISE
        )

    # Resize all images to the same dimensions
    image = cv2.resize(
        image,
        (TARGET_WIDTH, TARGET_HEIGHT),
        interpolation=cv2.INTER_AREA
    )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Find the checkerboard corners
    found, corners = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        None
    )

    if found:

        refined_corners = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            criteria
        )

        object_points.append(
            object_pattern.copy()
        )

        image_points.append(
            refined_corners
        )

        successful_images += 1

        print(
            f"SUCCESS: {os.path.basename(filename)}"
        )

    else:

        failed_images += 1

        print(
            f"FAILED: {os.path.basename(filename)}"
        )

# ---------------------------------------------------------
# CHECK THAT ENOUGH IMAGES WORKED
# ---------------------------------------------------------

if successful_images < 5:
    raise RuntimeError(
        "Not enough successful checkerboard images were detected."
    )

# ---------------------------------------------------------
# CAMERA CALIBRATION
# ---------------------------------------------------------

ret, camera_matrix, distortion_coefficients, rvecs, tvecs = (
    cv2.calibrateCamera(
        object_points,
        image_points,
        (TARGET_WIDTH, TARGET_HEIGHT),
        None,
        None
    )
)

# ---------------------------------------------------------
# CALCULATE MEAN REPROJECTION ERROR
# ---------------------------------------------------------

total_error = 0.0

for i in range(len(object_points)):

    projected_points, _ = cv2.projectPoints(
        object_points[i],
        rvecs[i],
        tvecs[i],
        camera_matrix,
        distortion_coefficients
    )

    observed = image_points[i].reshape(-1, 2).astype(np.float32)
    projected = projected_points.reshape(-1, 2).astype(np.float32)

    error = np.linalg.norm(
        observed - projected,
        axis=1
    ).mean()

    total_error += error

mean_reprojection_error = (
    total_error / len(object_points)
)

# ---------------------------------------------------------
# EXTRACT INTRINSIC CAMERA PARAMETERS
# ---------------------------------------------------------

fx = camera_matrix[0, 0]
fy = camera_matrix[1, 1]
cx = camera_matrix[0, 2]
cy = camera_matrix[1, 2]

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

print("\n--------------------------------------")
print("CAMERA CALIBRATION COMPLETE")
print("--------------------------------------")

print(f"\nSuccessful images: {successful_images}")
print(f"Failed images: {failed_images}")

print("\nNormalized image size:")
print(f"{TARGET_WIDTH} x {TARGET_HEIGHT} pixels")

print("\nCalibration RMS Error:")
print(ret)

print("\nMean Reprojection Error:")
print(mean_reprojection_error)

print("\nCamera Matrix K:")
print(camera_matrix)

print("\nDistortion Coefficients:")
print(distortion_coefficients)

print("\nIntrinsic Camera Parameters:")
print(f"fx = {fx}")
print(f"fy = {fy}")
print(f"cx = {cx}")
print(f"cy = {cy}")

# ---------------------------------------------------------
# SAVE RESULTS FOR STEP 2
# ---------------------------------------------------------

np.savez(
    "calibration_data.npz",
    camera_matrix=camera_matrix,
    distortion=distortion_coefficients,
    fx=fx,
    fy=fy,
    cx=cx,
    cy=cy,
    image_width=TARGET_WIDTH,
    image_height=TARGET_HEIGHT
)

print("\nCalibration data saved successfully.")
print("File created: calibration_data.npz")