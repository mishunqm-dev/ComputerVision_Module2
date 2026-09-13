import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# CSC 8830 - Computer Vision
# Module 2 Assignment Web Application
# ---------------------------------------------------------

st.set_page_config(
    page_title="Computer Vision Object Measurement",
    page_icon="📷",
    layout="wide"
)

st.title("📷 Smartphone Camera Calibration & Object Measurement")

st.write(
    """
    This application demonstrates smartphone camera calibration,
    perspective-projection-based real-world object measurement,
    and experimental error analysis.
    """
)

# ---------------------------------------------------------
# CAMERA CALIBRATION RESULTS
# ---------------------------------------------------------

st.header("1. Camera Calibration Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Successful Calibration Images", "16")
    st.metric("Calibration RMS Error", "0.8823 px")

with col2:
    st.metric("Mean Reprojection Error", "0.6515 px")
    st.metric("Camera Distance for Testing", "2.44 m")

st.subheader("Intrinsic Camera Parameters")

camera_data = pd.DataFrame({
    "Parameter": ["fx", "fy", "cx", "cy"],
    "Value": [
        948.6546978611518,
        950.4338898501043,
        513.2899322035433,
        679.2681635763906
    ]
})

st.dataframe(camera_data, use_container_width=True)

st.subheader("Camera Matrix K")

st.code(
    """
[[948.65469786,   0.00000000, 513.28993220],
 [  0.00000000, 950.43388985, 679.26816358],
 [  0.00000000,   0.00000000,   1.00000000]]
"""
)

st.subheader("Distortion Coefficients")

st.code(
    """
[0.22950183, -1.15152792, 0.00409115, 0.00521234, 1.92763582]
"""
)

# ---------------------------------------------------------
# PERSPECTIVE PROJECTION
# ---------------------------------------------------------

st.header("2. Perspective Projection Measurement")

st.write(
    """
    Real-world object dimensions were estimated using the calibrated
    focal lengths and a known camera-to-object distance.
    """
)

st.latex(r"W = \frac{wZ}{f_x}")
st.latex(r"H = \frac{hZ}{f_y}")

st.write(
    """
    Where:

    - **W** = estimated real-world width
    - **H** = estimated real-world height
    - **w** = object width in pixels
    - **h** = object height in pixels
    - **Z** = camera-to-object distance
    - **fx, fy** = calibrated focal lengths
    """
)

# ---------------------------------------------------------
# EXPERIMENTAL RESULTS
# ---------------------------------------------------------

st.header("3. Experimental Results")

results = pd.read_csv("results.csv")

st.dataframe(
    results,
    use_container_width=True
)

# ---------------------------------------------------------
# SUMMARY STATISTICS
# ---------------------------------------------------------

st.header("4. Error Statistics")

mae = results["Absolute Error (in)"].mean()

rmse = (
    (
        (results["Estimated (in)"] - results["Actual (in)"]) ** 2
    ).mean()
) ** 0.5

mape = results["Percent Error (%)"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Mean Absolute Error",
        f"{mae:.2f} in"
    )

with col2:
    st.metric(
        "RMSE",
        f"{rmse:.2f} in"
    )

with col3:
    st.metric(
        "Mean Absolute Percentage Error",
        f"{mape:.2f}%"
    )

# ---------------------------------------------------------
# ERROR CHART
# ---------------------------------------------------------

st.subheader("Percent Error by Measurement")

chart_data = results[
    ["Object", "Dimension", "Percent Error (%)"]
].copy()

chart_data["Measurement"] = (
    chart_data["Object"]
    + " - "
    + chart_data["Dimension"]
)

chart_data = chart_data.set_index("Measurement")

st.bar_chart(
    chart_data["Percent Error (%)"]
)

# ---------------------------------------------------------
# CONCLUSION
# ---------------------------------------------------------

st.header("5. Conclusion")

st.write(
    """
    The experiment demonstrates that calibrated smartphone images can
    be used with perspective projection equations to estimate real-world
    object dimensions.

    Flat, rigid, front-facing objects generally produced more accurate
    results than irregular or soft objects. Measurement error was
    influenced by camera alignment, object orientation, manual region
    selection, distance measurement, and lens distortion.
    """
)