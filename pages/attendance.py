import streamlit as st

from menu import menu_with_redirect
from utils import attendance_needed_subjects, get_bunk_subjects, get_user_data_in_tables

menu_with_redirect()

if "df_attendance" not in st.session_state:
    st.session_state.df_attendance = None

st.title("Subject Attendance")
st.divider()
st.header("Your Attendance")
with st.spinner("Fetching your attendance..."):
    attendance_url = "https://samvidha.iare.ac.in/home?action=stud_att_STD"
    attendance_table_selector = "body > div > div.content-wrapper > section.content > div.card.card-info > div.card-body.dataTables_wrapper > table"
    df = get_user_data_in_tables(st.session_state.login_cookie, attendance_url, attendance_table_selector)
    if df is not None:
        st.session_state.df_attendance = df
    else:
        st.error("Failed to fetch attendance data")
if st.session_state.df_attendance is None:
    st.stop()
st.dataframe(st.session_state.df_attendance, hide_index=True, use_container_width=True)
st.header("Needed Attendance")
st.write("You need to attend the following number of classes to achieve 75% attendance in each subject")
with st.spinner("Calculating needed attendance..."):
    new_df = attendance_needed_subjects(st.session_state.df_attendance, 75)
if new_df.empty:
    st.info("You have already achieved 75% attendance in all subjects")
else:
    st.dataframe(new_df, hide_index=True, use_container_width=True)
st.header("Bunk Predictor")
st.write("The number of classes you can bunk in subject to maintain 75% attendance")
with st.spinner("Calculating bunk count..."):
    new_df = get_bunk_subjects(st.session_state.df_attendance, 75)
if new_df.empty:
    st.info("You can't bunk any classes in any subject")
else:
    st.dataframe(new_df, hide_index=True, use_container_width=True)
