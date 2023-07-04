import streamlit as st
import Page_Codes

# st.set_page_config(page_title="Pharmacy App", page_icon=":pill:")


def login():
    st.title("Artemis Pharmacy")
    st.header("Welcome to Artemis Pharmacy. Please Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":
            session_state.login = True
            session_state.user_type = "admin"
        elif username == "user" and password == "user":
            session_state.login = True
            session_state.user_type = "user"
        else:
            st.error("Incorrect username or password")


session_state = st.session_state
if "login" not in session_state:
    session_state.login = False

if not session_state.login:
    login()
else:
    if session_state.user_type == "admin":
        Page_Codes.admin_login()
    else:
        Page_Codes.user_login()