from pathlib import Path

import cv2
import streamlit as st
import zipfile
import pandas as pd
import os
import shutil

from types import NoneType

from modules.inference import inference
from templates import TGSTAT_SEARCH_LIST
from modules.utils import MAIN_STAT

st.set_page_config(layout="wide")


def clear_path(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def exel_form():
    main_form = st.form("main_form", clear_on_submit=True)

    with main_form:
        # table = st.file_uploader("Choose a table", accept_multiple_files=False, type=['xlsx'])

        archive = st.file_uploader("Choose a archive with images", accept_multiple_files=False, type=['zip'])

        submitted = st.form_submit_button("Submit")

    if submitted:
        # if type(table) is NoneType:
        #     st.error('You have to choose an table!', icon="🚨")

        if type(archive) is NoneType:
            st.error('You have to choose an archive!', icon="🚨")

        else:
            # bytes_data = table.read()
            #
            # path = Path(Path(__file__).parents[1], 'tmp', 'table')
            #
            # with open(path, 'wb') as f:
            #     f.write(bytes_data)
            #
            # xl = pd.ExcelFile(path)
            # df = xl.parse('Sheet1')
            # st.dataframe(df)

            with st.spinner('Save and unzip archive'):

                bytes_data = archive.read()

                path = Path(Path(__file__).parents[1], 'tmp', 'archive')
                unzip = Path(Path(__file__).parents[1], 'tmp', 'unzip')

                with open(path, 'wb') as f:
                    f.write(bytes_data)

                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(unzip)

                new_unzip = None
                for file in unzip.glob('*'):
                    if os.path.isdir(file):
                        new_unzip = file
                        break
                    else:
                        new_unzip = unzip

            _, _, files = next(os.walk(str(new_unzip)))
            file_count = len(files)

            cost = 100/file_count

            results = []
            i = 0
            n = 0
            my_bar = st.progress(0, text=f"Image processing: {n}/{file_count}")
            for file in new_unzip.glob('*'):
                filename = file.name
                img = cv2.imread(str(file))

                res_img, _, matched_instances, user_instance = inference(img)

                res_dict = {"name": filename, "img": res_img}
                if user_instance:
                    res_dict["username"] = user_instance.value
                else:
                    res_dict["username"] = "unknown"

                for item in matched_instances:
                    res_dict[item.value] = item.match_instance.value

                results.append(res_dict)

                i += round(cost)
                n += 1
                my_bar.progress(i, text=f"Image processing: {n}/{file_count}")
            my_bar.progress(100, text=f"Image processing: Done!")

            clear_path(str(unzip))

            # show_result(results)

            download_result(results)


def download_result(results):

    options = st.multiselect('Select the parameters to be uploaded', MAIN_STAT)

    if options:
        df = pd.DataFrame(columns=options)
        for result in results:
            row = []
            for column in options:
                try:
                    row.append(result[column])
                except KeyError:
                    row.append("none")
            df.loc[-1] = row

        st.dataframe(df)

    download_form = st.form("download_form", clear_on_submit=True)

    with download_form:
        st.text("HUH")


def show_result(res):
    st.header("Results")

    col1, col2 = st.columns(2)

    with col1:
        for item in res:
            st.image(item['img'], channels="BGR")

    with col2:
        for item in res:
            st.write(item['name'])


if __name__ == "__main__":
    exel_form()
