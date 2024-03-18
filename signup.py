import streamlit as st
import psycopg2
from connectiondb import connect_to_db
def driver_signup():
    st.write("Driver Signup Form")
    email = st.text_input("Email", key="driver_email")
    password = st.text_input("Password", type="password", key="driver_password")
    name = st.text_input("Name", key="driver_name")
    # Add more fields as needed

    if st.button("Signup"):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_access (email, password, name, role) VALUES (%s, %s, %s, %s)",
                       (email, password, name, "driver"))
        conn.commit()
        st.success("Signup successful!")
        conn.close()


def customer_signup():
    st.write("Customer Signup Form")
    email = st.text_input("Email", key="customer_email")
    password = st.text_input("Password", type="password", key="customer_password")
    name = st.text_input("Name", key="customer_name")
    # Add more fields as needed

    if st.button("Signup"):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_access (email, password, name, role) VALUES (%s, %s, %s, %s)",
                       (email, password, name, "customer"))
        conn.commit()
        st.success("Signup successful!")
        conn.close()


def owner_signup():
    st.write("Owner Signup Form")
    email = st.text_input("Email", key="owner_email")
    password = st.text_input("Password", type="password", key="owner_password")
    name = st.text_input("Name", key="owner_name")
    # Add more fields as needed

    if st.button("Signup"):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_access (email, password, name, role) VALUES (%s, %s, %s, %s)",
                       (email, password, name, "owner"))
        conn.commit()
        st.success("Signup successful!")
        conn.close()
def signup():
    st.title("LogiLink Signup")
    role = st.selectbox("Choose Your Role", ("Driver", "Customer", "Owner"))
    if role == "Driver":
        driver_signup()
    elif role == "Customer":
        customer_signup()
    elif role == "Owner":
        owner_signup()

    if st.button("Go to Login Page"):
        st.session_state['page'] = 'login'