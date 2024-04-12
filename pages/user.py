import streamlit as st

from menu import menu_with_redirect

menu_with_redirect()

st.title(f"Welcome, {st.session_state.user_data['Full Name']}")
st.divider()
st.header("User Image")
st.image(st.session_state.user_data["image_url"], width=200)
st.header("User Details")
st.table({
    "Full Name": st.session_state.user_data["Full Name"],
    "Branch": st.session_state.user_data["Branch"],
    "Roll Number": st.session_state.user_data["Roll Number"],
    "Semester": st.session_state.user_data["Semester"],
    "Section": st.session_state.user_data["Section"]
})
