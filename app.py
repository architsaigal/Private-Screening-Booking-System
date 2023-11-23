import streamlit as st
import pandas as pd
import datetime as dt
from omdb_conn import OmdbAPIConnection
from helper_components import ColoredHeader, Notif, Setup
from account_creation import login, signup, Account_Creation
from browse_movies import Movie_Selection
from admin import Admin

def Siderbar():
    '''
    -------------------------------
    Sidebar Content
    -------------------------------
    Parameters:
        None

    Returns:
        None
    '''
    with st.sidebar:
        st.title("SE Project")
        st.write("Private Screening Booking System")
        # write 4 line of same text
        st.write("This is a private screening booking system for the SE project.")
        st.write()
        st.session_state['search_bar'] = st.text_input(
            label="Movie Name",
            value="Batman",
            )

        if st.button("Choose Moive"):
            st.session_state['movie_choice'] = None
            st.session_state['movie_df'] = None
            st.cache_data.clear()
            st.rerun()

        # if st.checkbox("Debug Mode",):
        #     st.subheader("Session State")
        #     st.write(st.session_state)

def session_state_management():
    '''
    -------------------------------
    Initialize session state values
    -------------------------------
    Parameters:
        None

    Returns:
        None
    '''
    if 'first_run' not in st.session_state:
        st.session_state['first_run'] = True
    if 'booking_first_run' not in st.session_state:
        st.session_state['booking_first_run'] = True
    if 'movie_df' not in st.session_state:
        st.session_state['movie_df'] = None
    if 'search_bar' not in st.session_state:
        st.session_state['search_bar'] = None
    if 'movie_choice' not in st.session_state:
        st.session_state['movie_choice'] = None
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'cost' not in st.session_state:
        st.session_state['cost'] = 0
    if 'user_details' not in st.session_state:
        st.session_state['user_details'] = {}
    if 'adm' not in st.session_state:
        st.session_state['adm'] = False
def main():
    # Page Setup
    Setup(
        page_title="Private Screening Booking System",
        page_icon="🎥",
        hide_streamlit_style=False,
        initial_sidebar_state="expanded",
    )
    # Page Title
    ColoredHeader(
        label="Private Screening Booking System",
        description="SE Project"
    )

    # Sidebar Content
    Siderbar()
    # Initialize session state
    session_state_management()

    if Account_Creation():
        if st.session_state['user'] == "admin":
            Admin()
        else:
            # Movie Selection
            Movie_Selection()
            
            # Logout Button
            _,col = st.columns([7,1])
            with col:
                if st.button("Logout"):
                    st.session_state["user"] = None
                    st.rerun()
            

if __name__ == "__main__":
    main()