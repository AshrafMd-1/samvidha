import streamlit as st
from menu import menu_with_redirect
from Utils.bio import display_bio_update_info, calculate_bio_attendance, calculate_bio_attend_or_bunk, get_user_bio

menu_with_redirect()

if "df_bio" not in st.session_state:
    st.session_state.df_bio = None

if "current_bio" not in st.session_state:
    st.session_state.current_bio = None

st.title("Biomteric Attendance")
st.divider()
if st.session_state.df_bio is None:
    with st.spinner("Fetching your biometric attendance..."):
        df = get_user_bio(st.session_state.login_cookie)
        if df is not None:
            st.session_state.df_bio = df
            st.rerun()
        else:
            st.error("Failed to fetch attendance data")
else:
    updated_date_df = display_bio_update_info(st.session_state.df_bio)
    if updated_date_df:
        st.warning(updated_date_df)
    with st.spinner("Calculating your biometric attendance..."):
        st.session_state.current_bio = calculate_bio_attendance(st.session_state.df_bio, 0)
        if st.session_state.current_bio is None:
            st.error("Failed to calculate your biometric attendance")

    st.header(f"Your Biometric Attendance - {st.session_state.current_bio:.2f}%")
    st.dataframe(st.session_state.df_bio, hide_index=True, use_container_width=True)
    st.table(st.session_state.df_bio["Status"].value_counts())
    refresh = st.button("Refresh")
    if refresh:
        st.session_state.df_bio = None
        st.session_state.current_bio = None
        st.rerun()
    if st.session_state.current_bio < 80:
        with st.spinner("Calculating needed attendance..."):
            st.header(
                f"Need to attend *{calculate_bio_attend_or_bunk(st.session_state.df_bio, 'attend')}* day(s)")
            st.write("to achieve 80% attendance")
    else:
        with st.spinner("Calculating bunk count..."):
            if not st.session_state.being_absent["status"]:
                st.header(f"Can bunk for {calculate_bio_attend_or_bunk(st.session_state.df_bio, 'bunk')} day(s)")
            else:
                st.header(
                    f"Can bunk for {calculate_bio_attend_or_bunk(st.session_state.df_bio, 'bunk', st.session_state.being_absent['count'])} day(s)")
            st.write("to maintain 80% attendance")
