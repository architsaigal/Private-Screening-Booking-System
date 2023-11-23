import streamlit as st

def Admin():
    st.write("Admin Page")
    conn = st.connection('mysql', type='sql')
    # Perform query.
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("User Data")
        user_df = conn.query('SELECT * from users;', ttl=600)
        st.write(user_df)
    with col2:
        st.subheader("Locations")
        locations_df = conn.query('SELECT * from locations;', ttl=600)
        st.write(locations_df)

    col3,col4 = st.columns(2)
    with col3:
        st.subheader("Bookings")
        booking_df = conn.query('SELECT * from bookings;', ttl=600)
        st.write(booking_df)
    with col4:
        st.subheader("Payments")
        payment_df = conn.query('SELECT * from payments;', ttl=600)
        st.write(payment_df)

    if st.button("Back"):
        st.session_state["movie_choice"] = 234
        st.session_state["movie_df"] =4566
        st.rerun()
        st.rerun()