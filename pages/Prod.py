import streamlit as st


st.set_page_config(layout="wide")


def exel_form():

    main_form = st.form("main_form", clear_on_submit=True)

    with main_form:
        table = st.file_uploader("Choose a table", accept_multiple_files=False, type=['xlsx'])

        option = st.selectbox(
            'You can choose the type of media source or use auto-detection',
            ('Auto', 'Telegram', 'VK', 'Yandex Dzen', 'YouTube'))

        submitted = st.form_submit_button("Submit")