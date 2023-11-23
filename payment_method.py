import streamlit as st
import mysql.connector as mysql
import pandas as pd
def Payment_Method():
    # payement method
    st.subheader ("Payment Method💳")
    with st.expander("Payment Method", expanded=True):
        payment_method_col, cost_col = st.columns([1,1])

        # Payment Method Radio Button
        with payment_method_col:
            payment_method = st.radio(
            label="Select Payment Method",
            options=["Credit Card", "Debit Card", "UPI"],
            )


        st.session_state["user_details"]["Payment_Method"] = payment_method
        
        # Payment Method Details
        if payment_method in ['Credit Card','Debit Card']:
            card_number = st.text_input(
                label="Card Number",
                placeholder="XXXX-XXXX-XXXX-XXXX",
                max_chars=19
                )
            card_expiry = st.text_input(
                label="Card Expiry",
                placeholder="MM/YY",
                max_chars=5
                )
            card_cvv = st.text_input(
                label="Card CVV",
                placeholder="XXX",
                max_chars=3
                )
            
            st.session_state['user_details']['card_no'] = card_number
            st.session_state['user_details']['card_exp'] = card_expiry
            st.session_state['user_details']['card_cvv'] = card_cvv
        elif payment_method == 'UPI':
            upi_id = st.text_input(
                label="UPI ID",
                placeholder="upi_id@bank",
                )
        
        
def Payment_Method_DataBase():
    conn = mysql.connect(host="localhost", user="root", password="root", database="se_project")
    cursor = conn.cursor()
    # get df of bookings table
    query = "SELECT * FROM bookings"
    # Use pandas to read the SQL query result into a DataFrame
    bookings_df = pd.read_sql(query, conn)
    
    
    # add user_id, booking_id, amount, payment_method
    cursor.execute(f"INSERT INTO payments (user_id, booking_id, amount, payment_method) VALUES ('{st.session_state['user_details']['user_id']}','{len(bookings_df) + 1}','{st.session_state['user_details']['Cost']}','{st.session_state['user_details']['Payment_Method']}')")
    conn.commit()
    conn.close()