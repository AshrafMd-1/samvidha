import time

import streamlit as st

from menu import menu
from utils import login_to_samvidha, get_user_details

if "login_cookie" not in st.session_state:
    st.session_state.login_cookie = None

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "Full Name": None,
        "image_url": None,
        "Branch": None,
        "Roll Number": None,
        "Semester": None,
        "Section": None,

    }

if st.session_state.login_cookie is not None and st.session_state.user_data["Full Name"] is not None:
    st.session_state.login_cookie = None
    st.session_state.user_data = {
        "Full Name": None,
        "image_url": None,
        "Branch": None,
        "Roll Number": None,
        "Semester": None,
        "Section": None
    }
    st.success("Logged out successfully")
    time.sleep(1)
    st.rerun()
else:
    with st.form("auth_form"):
        st.write("Login to Samvidha")
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.status("Authentication Process Running...", expanded=False) as status:
                st.write("Initializing...")
                logged_user = login_to_samvidha(username, password)
                if logged_user["status"]:
                    st.write("Logged in successfully")
                    st.session_state.login_cookie = logged_user["cookies"]
                    if st.session_state.user_data["Full Name"] is None:
                        st.write("Fetching user details...")
                        user_details = get_user_details(st.session_state.login_cookie)
                        if user_details["Full Name"] is not None:
                            status.update(label="User details fetched successfully", state="complete", expanded=False)
                            st.session_state.user_data = user_details
                            time.sleep(1)
                            st.switch_page("pages/user.py")
                        else:
                            status.update(label="Failed to fetch user details", state="error", expanded=False)
                            st.session_state.login_cookie = None
                    else:
                        status.update(label="User details already fetched", state="complete", expanded=False)
                        time.sleep(1)
                        st.switch_page("pages/user.py")
                else:
                    status.update(label=logged_user["msg"], state="error", expanded=False)

menu()
