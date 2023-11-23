import streamlit as st
from helper_components import ColoredHeader, Notif
import mysql.connector as mysql

def login():
    '''
    -------------------------------------------
    Login Page
    -------------------------------------------
    Description:
        This function is used to login to an existing account. 
        if authentication is successful, the user is logged in and the session state variable "user" is set to the username.
        if authentication is unsuccessful, an error message is displayed.

    Parameters:
        None

    Returns:
        None
    '''
    def authenticate(user, password):
        '''
        -------------------------------------------
        Authentication
        -------------------------------------------
        Description:
            This function is used to authenticate the user.

        Parameters:
            user (str): username
            password (str): password

        Returns:
            True if authentication is successful, False otherwise
        '''
        # -------------------------------------------
        # TODO: Add authentication logic here using DBMS
        # -------------------------------------------

        if (user == "admin" and password == "admin"):
            return "admin"

        else:
            conn = mysql.connect(host="localhost", user="root", password="root", database="se_project")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE username='{user}'")
            result = cursor.fetchall()
            conn.close()

            if result[0][2] == password:
                st.session_state['user_details']['user_id'] = result[0][0]    
                return True
                st.write("True")
            else:
                return False

    st.title("Login Page")

    if st.session_state['adm']:
        username = st.text_input("Enter Username",value="admin")
        password = st.text_input("Enter Password", type="password", placeholder="Enter password" ,value="admin" )
    else:
        username = st.text_input("Enter Username",value="Alice")
        password = st.text_input("Enter Password", type="password", placeholder="Enter password" ,value="Tiger123" )
 
    if st.button(label="Login"):
        if authenticate(username,password) == "admin":
            st.session_state["user"] = "admin"
        elif authenticate(username,password):
            st.session_state["user"] = username
        else:
            Notif("error", 2, "Invalid user name or password.")


        
def signup():

    def on_signup_click():
        '''
        -------------------------------------------
        Signup
        -------------------------------------------
        Description:
            This function is used to create a new account.
            Checks if the username and password are valid and if the passwords match.

        Parameters:
            None

        Returns:
            True if signup is successful, False otherwise
        '''

        if s_password == s_confirm_password:
            if s_username != "" and s_password != "":
                conn = mysql.connect(host="localhost", user="root", password="root", database="se_project")
                cursor = conn.cursor()
                if len(result) == 0:
                    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{s_username}', '{s_password}')")
                    conn.commit()
                    conn.close()
                    return True
                else:
                    conn.close()
                    return False
        return False
        
    st.title("Signup Page")

    s_username = st.text_input("Username", placeholder="Enter username")
    s_password = st.text_input("Password", type="password", placeholder="Enter password")
    s_confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")

    if st.button("Signup"):
        if on_signup_click():
            Notif("success", 2, "Signup successful!")
        else:
            Notif("error", 2, "Signup unsuccessful.")
            
def Account_Creation():
    '''
    -------------------------------------------
    Account Creation
    -------------------------------------------
    Description:
        This function is used to create a new account or login to an existing account.

    Parameters:
        None

    Returns:
        True if the user is logged in, False otherwise
    '''
    # if st.session_state.setdefault("user", None) is None:
    if st.session_state["user"] is None:
        login_tab, signup_tab = st.tabs(["Login", "Signup"])
        with login_tab:
            login()
        with signup_tab:
            signup()
    else:
        if st.session_state["first_run"]:
            st.session_state["first_run"] = False
            # this prevents the toast from showing up every time the page is refreshed and only shows up once
            st.toast(f"Welcome back! {st.session_state['user']}👋")
        return True
