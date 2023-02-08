# Import libraries
import numpy as np
import streamlit as st
from PIL import Image

from detector.image_process import draw_bboxes, draw_labels, resize_keep_ratio
from detector.vibrio_detector import VibrioDetector

vibrioDetector = VibrioDetector()

st.set_page_config(layout="wide")

# Add a header in side bar
st.sidebar.markdown(
    '<p class="font">Vibrio Detector and Estimator</p>',
    unsafe_allow_html=True)

st.sidebar.write("""
    An application to estimate the total number and size of each vibrio.
    By using image processing technique to localize the vibrio and mathematical
    calculation for estimating the size of each vibrio
    """)

st.markdown(
    """
    <style>
        .font {
            font-size: 35px;
            font-family: 'Cooper Black';
            color: #5EBD99;
        }
    </style>
    """,
    unsafe_allow_html=True)

st.markdown(
    '<p class="font">Upload your photo here...</p>',
    unsafe_allow_html=True)

# Add file uploader to allow users to upload photos
uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'])

# Add 2 col for images
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Vibrio Image</p>',
                    unsafe_allow_html=True)
        st.image(image, width=None)

    with col2:
        st.markdown('<p style="text-align: center;">Detection</p>',
                    unsafe_allow_html=True)

        input_image = np.asarray(image)
        detection = vibrioDetector.run(image=input_image)

        osd_image = resize_keep_ratio(
            image=input_image, max_size=640)
        osd_image = draw_bboxes(
            image=osd_image, detection=detection)
        osd_image = draw_labels(
            image=osd_image, detection=detection)

        st.image(osd_image, width=None)

    st.markdown(
        '<p>Yellow Vibrio: {}</p>'.format(len(detection['boxes'])),
        unsafe_allow_html=True)

    st.markdown(
        '<p>Green Vibrio: 0</p>',
        unsafe_allow_html=True)
