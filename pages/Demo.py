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

        option = st.selectbox(
            'You can choose the type of media source or use auto-detection',
            ('Auto', 'Telegram', 'VK', 'Yandex Dzen', 'YouTube'))

        submitted = st.form_submit_button("Submit")

    if submitted:
        if type(image) is NoneType:
            st.error('You have to choose an image!', icon="🚨")

        else:
            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)

            opencv_image = cv2.imdecode(file_bytes, 1)
            original = opencv_image.copy()

            with st.spinner('Wait for it...'):
                start = time.time()
                res = inference(opencv_image)
                end = time.time() - start

            # res_show = cv2.resize(res, (0,0), fx=0.5, fy=0.5)

            show_result(original, res, opencv_image, end)


def show_result(original, detection, match, time):

    st.header("Results")

    col1, col2 = st.columns(2)

    with col1:
        st.image(original, channels="BGR")
        st.image(detection, channels="BGR")
        # st.image(match, channels="BGR")

    with col2:
        st.text("Original image and the detected numbers and text.")
        st.text(f"Elapsed time: {time}")


if __name__ == "__main__":
    demo()
