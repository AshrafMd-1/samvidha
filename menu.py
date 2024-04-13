import streamlit as st


def authenticated_menu():
    st.sidebar.page_link("pages/user.py", label="Your profile")
    st.sidebar.page_link("pages/attendance.py", label="Attendance")
    st.sidebar.page_link("pages/pat.py", label="Pat")
    st.sidebar.page_link("pages/biometric.py", label="Biometric")
    st.sidebar.page_link("pages/about.py", label="About")
    st.sidebar.page_link("app.py", label="Logout")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")
    st.sidebar.page_link("pages/about.py", label="About")


def menu():
    if "login_cookie" not in st.session_state or st.session_state.login_cookie is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    if "login_cookie" not in st.session_state or st.session_state.login_cookie is None:
        st.switch_page("app.py")
    menu()
