import math as Math

import streamlit as st

from menu import menu_with_redirect
from utils import get_user_bio, \
    calculate_bio_attendance, calculate_bio_attend_or_bunk

menu_with_redirect()

if "df_bio" not in st.session_state:
    st.session_state.df_bio = None

if "current_bio" not in st.session_state:
    st.session_state.current_bio = None

st.title("Biomteric Attendance")
st.divider()
with st.spinner("Fetching your biometric attendance..."):
    df = get_user_bio(st.session_state.login_cookie)
    if df is not None:
        st.session_state.df_bio = df
    else:
        st.header("Your Biometric Attendance")
        st.error("Failed to fetch attendance data")
if st.session_state.df_bio is None:
    st.stop()
st.session_state.current_bio = calculate_bio_attendance(st.session_state.df_bio)
st.header(f"Your Biometric Attendance - {st.session_state.current_bio:.2f}%")
st.dataframe(st.session_state.df_bio, hide_index=True, use_container_width=True)
if Math.floor(st.session_state.current_bio) < 75:
    with st.spinner("Calculating needed attendance..."):
        st.header(f"Need to attend {calculate_bio_attend_or_bunk(st.session_state.df_bio, 'attend')} day(s)")
else:
    with st.spinner("Calculating bunk count..."):
        st.header(f"Can bunk for {calculate_bio_attend_or_bunk(st.session_state.df_bio, 'bunk')} day(s)")
