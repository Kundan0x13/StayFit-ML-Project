import streamlit as st
from services.persistence.exercise_repository import get_or_create_user

def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True
    
    st.title("StayFit : AI Gym Coach")
    st.markdown("Welcome to StayFit! Login to start your fitness journey.")
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter a unique username")
        submit_button = st.form_submit_button("Login", width="stretch")
    
    if submit_button:
        if username:
            user = get_or_create_user(username)
            st.session_state["user_id"] = user["id"]
            st.session_state["username"] = user["username"]
            st.success(f"Logged in as {username}")
            st.rerun()
            return True
        else:
            st.error("Please enter a valid username.")
            return False
    
    
    return False

