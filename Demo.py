import time
from pathlib import Path

import streamlit as st
import cv2
import os
import numpy as np
import pandas as pd

# from types import NoneType

from modules.inference import inference


st.set_page_config(layout="wide")


def demo():
    main_form = st.form("main_form", clear_on_submit=True)

    with main_form:
        image = st.file_uploader("Choose a image", accept_multiple_files=False, type=['jpg', 'png'])

        submitted = st.form_submit_button("Submit")

    if submitted:
        # if type(image) is NoneType:
        if False:
            st.error('You have to choose an image!', icon="🚨")

        else:
            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)

            opencv_image = cv2.imdecode(file_bytes, 1)
            original = opencv_image.copy()

            with st.spinner('Image processing'):
                img_det, img_match, matched_instances, user_instance, platform = inference(opencv_image)

            # res_show = cv2.resize(res, (0,0), fx=0.5, fy=0.5)

            show_result(original, img_det, img_match, matched_instances, user_instance, platform)


def show_result(original, detection, match, matches, user_instance, platform):

    st.header("Results")

    st.image(match, channels="BGR")

    st.text("Original image and the detected numbers and text.")
    st.text("Matched instances:")

    col1, col2, col3 = st.columns(3)
    user_name = user_instance.value if user_instance is not None else 'Unknown'
    col1.metric("User", f"{user_name}")
    col2.metric("Platform", f"{platform}")
    col1, col2, col3 = st.columns(3)
    for idx, mm in enumerate(matches):
        num = idx % 3
        if num == 0:
            col1.metric(f"{mm.value}", f"{mm.match_instance.value}")
        elif num == 1:
            col2.metric(f"{mm.value}", f"{mm.match_instance.value}")
        elif num == 2:
            col3.metric(f"{mm.value}", f"{mm.match_instance.value}")


if __name__ == "__main__":
    demo()
