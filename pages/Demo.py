import time
from pathlib import Path

import streamlit as st
import cv2
import os
import numpy as np
import pandas as pd

from types import NoneType

from modules.inference import inference


st.set_page_config(layout="wide")


def demo():
    main_form = st.form("main_form", clear_on_submit=True)

    with main_form:
        image = st.file_uploader("Choose a image", accept_multiple_files=False, type=['jpg', 'png'])

        submitted = st.form_submit_button("Submit")

    if submitted:
        if type(image) is NoneType:
            st.error('You have to choose an image!', icon="🚨")

        else:
            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)

            opencv_image = cv2.imdecode(file_bytes, 1)
            original = opencv_image.copy()

            with st.spinner('Image processing'):
                img_det, img_match, matched_instances, user_instance = inference(opencv_image)

            # res_show = cv2.resize(res, (0,0), fx=0.5, fy=0.5)

            show_result(original, img_det, img_match, matched_instances, user_instance)


def show_result(original, detection, match, matches, user_instance):

    st.header("Results")

    col1, col2 = st.columns(2)

    with col1:
        # st.image(original, channels="BGR")
        # st.image(detection, channels="BGR")
        st.image(match, channels="BGR")

    with col2:
        with st.container():
            st.text("Original image and the detected numbers and text.")
            st.text("Matched instances:")
            # st.text(f"User: {user_instance.value}")
            st.metric("User", f"{user_instance.value}")
            col1, col2, col3 = st.columns(3)
            for idx, mm in enumerate(matches):
                num = idx % 3
                if num == 0:
                    col1.metric(f"{mm.value}", f"{mm.match_instance.value}")
                elif num == 1:
                    col2.metric(f"{mm.value}", f"{mm.match_instance.value}")
                elif num == 2:
                    col3.metric(f"{mm.value}", f"{mm.match_instance.value}")
                # st.text(f"Key: {mm.value} ; Value: {mm.match_instance.value}")


if __name__ == "__main__":
    demo()
