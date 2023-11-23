import streamlit as st
import pandas as pd
import datetime as dt
from omdb_conn import OmdbAPIConnection
from booking_movie import Booking_Movie, Booking_Movie_DataBase
from payment_method import Payment_Method, Payment_Method_DataBase
from helper_components import Notif
def Movie_Selection():
    if st.session_state["movie_choice"] is None:
        st.title("Browse Movies")
        st.write("Select a movie to book a private screening.")
        
        # Setting up the API connection
        imdb_conn = OmdbAPIConnection("IMDB Connection" , api_key = st.secrets["api_key"])
        df = imdb_conn.query(
            name=st.session_state['search_bar'],
            type="movie",
            full_information=True,
            )

        # st.dataframe(df)

        st.write()
        st.divider()

        # Displaying the movies
        for df_row in range(len(df)):
            movie = df.iloc[df_row]
            image_col, info_col, year_col = st.columns([3, 7, 1.5])
            with image_col:
                st.image(
                    str(movie["Poster"]),
                    width=150, # Manually Adjust the width of the image as per requirement
                )
            with info_col:
                st.subheader(movie["Title"])
                st.write(movie['Plot'])

                # Used to book the movie and go to the next page
                if st.button("Book Now", key=df_row):
                    st.session_state["movie_choice"] = movie["Title"]
                    st.session_state["movie_df"] = movie
                    st.rerun()
            with year_col:
                st.caption(f"Year: {movie['Year']}")
                st.caption(f"Rating: {movie['imdbRating']}⭐")
            st.divider()

    else:
        # when movie is selected
        if st.session_state["booking_first_run"]:
            # this prevents the toast from showing up every time the page is refreshed and only shows up once
            st.session_state["booking_first_run"] = False
            st.toast(f"Booking {st.session_state['movie_choice']}...")

        st.title("Booking Details")

        # Displaying the movie details
        movie = st.session_state["movie_df"]
        st.session_state['user_details']['movie_id'] = movie.imdbID

        image_col, info_col, year_col = st.columns([3, 7, 1.5])
        with image_col:
            st.image(
                str(movie["Poster"]),
                width=150, # Manually Adjust the width of the image as per requirement
            )
        with info_col:
            st.subheader(movie["Title"])
            st.write(movie['Plot'])
        with year_col:
            st.caption(f"Year: {movie['Year']}")
            st.caption(f"Rating: {movie['imdbRating']}⭐")
        st.divider()

        # Displaying the booking details
        payment_method_col,movie_detail_col = st.columns([1, 1])

        with payment_method_col:
            Payment_Method()
        with movie_detail_col:
            Booking_Movie()

        
        # Confirm Booking Button
        confirm_booking_col, back_col = st.columns([7,1])
        with confirm_booking_col:
            if st.button("Confirm Booking"):
                if any(value == "" for value in st.session_state['user_details'].values()):
                    Notif("error",message="Please fill out all details")
                else:
                    st.success("Booking Confirmed")
                    st.balloons()
                    Booking_Movie_DataBase()
                    Payment_Method_DataBase()
                    st.stop()
        # Back Button to go back to the movie selection page
        with back_col:
            if st.button("Back"):
                st.session_state["movie_choice"] = None
                st.session_state["movie_df"] = None
                st.rerun()