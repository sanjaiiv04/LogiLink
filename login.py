import streamlit as st
from connectiondb import connect_to_db
def driver_login():
    st.write("Driver Login Form")
    email = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    if login_button:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_access WHERE role = 'driver' AND username = %s AND password = %s",
                       (email, password))
        result = cursor.fetchone()
        if result:
            st.session_state['page'] = 'dashboard'
            st.session_state['role'] = 'driver'
        else:
            st.error("Invalid credentials")
        cursor.close()
        conn.close()


def owner_login():
    st.write("Owner Login Form")
    email = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    if login_button:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_access WHERE role = 'owner' AND username = %s AND password = %s",
                       (email, password))
        result = cursor.fetchone()
        if result:
            st.session_state['page'] = 'dashboard'
            st.session_state['role'] = 'owner'
        else:
            st.error("Invalid credentials")
        cursor.close()
        conn.close()


def customer_login():
    st.write("Customer Login Form")
    email = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    if login_button:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_access WHERE role = 'customer' AND username = %s AND password = %s",
                       (email, password))
        result = cursor.fetchone()
        if result:
            st.session_state['page'] = 'dashboard'
            st.session_state['role'] = 'customer'
        else:
            st.error("Invalid credentials")
        cursor.close()
        conn.close()
def login():
    st.title("LogiLink Login Portal")
    role = st.selectbox("Choose Your Role", ("Driver", "Customer", "Owner"), key="role_select")
    if role == "Driver":
        driver_login()
    elif role == "Customer":
        customer_login()
    elif role == "Owner":
        owner_login()

    if st.button("Go to Signup Page"):
        st.session_state['page'] = 'signup'