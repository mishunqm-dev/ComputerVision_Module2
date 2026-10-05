# Smartphone Camera Calibration & Object Measurement

This project uses Python and OpenCV to calibrate a smartphone camera and estimate real-world object dimensions using perspective projection. The project evaluates measurement accuracy through experimental error analysis and includes a Streamlit application for presenting calibration and measurement results.

## Technologies Used

- Python
- OpenCV
- NumPy
- Pandas
- Streamlit
- Computer Vision
- Camera Calibration
- Perspective Projection

## Features

- Smartphone camera calibration using a checkerboard pattern
- Camera intrinsic parameter estimation
- Lens distortion coefficient estimation
- Real-world object measurement using perspective projection
- Experimental comparison of estimated and actual object dimensions
- Error analysis using MAE, RMSE, and percentage error
- Streamlit web application for displaying calibration and measurement results

## Camera Calibration Results

- Successful calibration images: 16
- Calibration RMS Error: 0.8823 px
- Mean Reprojection Error: 0.6515 px

Intrinsic camera parameters:

- fx = 948.6547
- fy = 950.4339
- cx = 513.2899
- cy = 679.2682

Camera-to-object testing distance:

- 2.44 meters
- 8 feet

## Perspective Projection

Real-world dimensions were estimated using:

W = (w × Z) / fx

H = (h × Z) / fy

Where:

- W = estimated real-world width
- H = estimated real-world height
- w = object width in pixels
- h = object height in pixels
- Z = camera-to-object distance
- fx, fy = calibrated focal lengths

## Experimental Results

The experiment used 10 objects for a total of 20 width and height measurements.

Overall error statistics:

- Mean Absolute Error: 3.55 inches
- RMSE: 4.37 inches
- Mean Absolute Percentage Error: 18.09%

The most accurate measurement was the width of the I AM framed poster, with approximately 0.83% error.

The largest percentage error occurred for the yellow pillow height, with approximately 41.24% error.

## Project Files

- `calibrate_camera.py` - performs camera calibration
- `measure_object.py` - estimates real-world object dimensions
- `check_images.py` - checks calibration/test image dimensions
- `app.py` - Streamlit web application
- `results.csv` - experimental measurement results
- `calibration_data.npz` - saved camera calibration parameters
- `calibration_images/` - checkerboard calibration images
- `test_images/` - object measurement images

## Run the Web Application

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the Streamlit application:

```bash
python3 -m streamlit run app.py
```
## Project Purpose

This project was developed as part of graduate-level Computer Vision coursework to explore practical applications of camera calibration, perspective projection, real-world object measurement, and experimental error analysis.
