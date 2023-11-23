import streamlit as st
import datetime as dt
from payment_method import Payment_Method
import mysql.connector as mysql
import pandas as pd
import random as rd
def Booking_Movie():
    # Booking Details
    st.subheader ("Booking Details🎬")
    with st.expander("Booking Details", expanded=True):
        # Booking Details
        date = st.date_input(
            label="Date",
            min_value=dt.date.today(),
            format="DD/MM/YYYY",
            )
        time = st.time_input(
            label="Time",
            value='now',
            )

        theatre = st.selectbox(
            label="Select Theatre",
            options=Cinema_Locations(),
            )
        
        # get capacity where thearte = mall_name
        df = Cinema_Locations_df()
        for i in range(len(df)):
            if df.iloc[i,1] ==  theatre:
                cap = df.iloc[i,2]
                st.session_state['cost'] = cap * 200
        
        st.subheader(f"Capacity: `{cap}`")

        # Displaying the Booking Cost
        st.metric(
            label="Cost",
            value=f"💵 {st.session_state['cost']} INR",
            delta="",
            delta_color="inverse",
            )

        st.session_state['user_details']["Location"] = theatre
        st.session_state['user_details']["Cost"] = st.session_state['cost']
        st.session_state['user_details']["Date"] = str(date)
        st.session_state['user_details']["Time"] = str(time)

def Cinema_Locations_df(filters = ""):
    # List of all cinema locations
    conn = mysql.connect(host="localhost", user="root", password="root", database="se_project")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM locations {filters}")
    result = cursor.fetchall()
    conn.close()
    # make df with id as index
    df = pd.DataFrame(result)
    return df

def Cinema_Locations():
    df = Cinema_Locations_df()
    min_cap = st.slider("Select Min Capacity",min(df[2]),max(df[2]),value=max(df[2]))
    df = df[df[2] >= min_cap]
    return df[1].tolist()
    # return [i[1] for i in result]

def Booking_Movie_DataBase():
    conn = mysql.connect(host="localhost", user="root", password="root", database="se_project")
    cursor = conn.cursor()
    # Using parameterized query to avoid SQL injection
    query = "INSERT INTO bookings (user_id, movie_id, location) VALUES (%s, %s, %s)"
    # Assuming 'Location' in st.session_state['user_details'] is a string, and 'user_id' and 'movie_id' are integers
    values = (st.session_state['user_details']['user_id'], st.session_state['user_details']['movie_id'], st.session_state['user_details']['Location'])
    # Execute the query with parameterized values
    cursor.execute(query, values)
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()