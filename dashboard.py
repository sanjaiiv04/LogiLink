import streamlit as st
import pandas as pd
from connectiondb import connect_to_db
import random
def dashboard(role):
    st.title(f"LogiLink {role.capitalize()} Dashboard")
    st.sidebar.title("Navigate")

    if role == 'owner':
        page = st.sidebar.radio("Select Page", ("My Info", "My Location", "Verification Portal"))
        if page == "My Info":
            st.write("Owner's Info Page")
            logout_status = st.button("Logout")
            if logout_status:
                st.session_state['page'] = None
        elif page == "My Location":
            st.write("Package Location Page")
            # Display map with predefined GPS locations
            st.map(pd.DataFrame({
                "latitude": [37.7749, 40.7128, 51.5074],
                "longitude": [-122.4194, -74.0060, -0.1278],
                "name": ["Location 1", "Location 2", "Location 3"]
            }))
        elif page == "Verification Portal":
            st.write("Owner's Verification Portal Page")
            username_otp = st.text_input("Enter username of driver")
            fullfilled_status = False

            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT driver_alloted FROM generate_otp_to_owner WHERE fullfilled = %s",
                           (fullfilled_status,))
            result_fullfilled = cursor.fetchall()  # Fetch all rows

            if result_fullfilled:
                # Convert the result to a list of driver alloted
                driver_alloted_list = [row[0] for row in result_fullfilled]
                df = pd.DataFrame(driver_alloted_list, columns=['Driver Alloted'])
                st.write(df)
            else:
                st.warning("No unfulfilled records found.")
            owner_otp_status = st.button("Generate OTP")
            if owner_otp_status:
                random_number = random.randint(1000, 9999)
                cursor.execute("update generate_otp_to_owner set otp=%s where driver_alloted= %s;",
                               (str(random_number), username_otp))
                conn.commit()
            conn.close()

    if role == 'driver':
        page = st.sidebar.radio("Select Page", ("My Info", "My Location", "Verification Portal", "Request OTP"))
        if page == "My Info":
            st.write("Driver's Info Page")
            logout_status = st.button("Logout")
            if logout_status:
                st.session_state['page'] = None
        elif page == "My Location":
            st.write("Driver's Location Page")
            # Display map with predefined GPS locations
            st.map(pd.DataFrame({
                "latitude": [37.7749, 40.7128, 51.5074],
                "longitude": [-122.4194, -74.0060, -0.1278],
                "name": ["Location 1", "Location 2", "Location 3"]
            }))
        elif page == "Request OTP":
            st.write("Driver's OTP Request Page")
            username_otp = st.text_input("Enter username of driver")
            package_otp = st.text_input("Enter package details")

            if st.button("Verify"):
                conn = connect_to_db()
                cursor = conn.cursor()
                query = "SELECT driver_alloted, package_details FROM driver_owner_verification WHERE driver_alloted = %s AND package_details = %s"
                cursor.execute(query, (username_otp, package_otp))
                results_from_query = cursor.fetchone()
                if results_from_query:
                    # Get the owner_alloted from driver_owner_verification
                    owner_alloted_query = "SELECT owner_alloted FROM driver_owner_verification WHERE driver_alloted = %s"
                    cursor.execute(owner_alloted_query, (username_otp,))
                    owner_alloted_result = cursor.fetchone()

                    if owner_alloted_result:
                        owner_alloted = owner_alloted_result[0]
                        insert_query = "INSERT INTO generate_otp_to_owner (driver_alloted, owner_alloted, fullfilled) VALUES (%s, %s, %s)"
                        cursor.execute(insert_query, (username_otp, owner_alloted, False))
                        conn.commit()
                        st.success("OTP Request successful!")
                    else:
                        st.error("Owner not found for the given driver.")
                else:
                    st.error("OTP Request failed! Please check your username and package details.")

                conn.close()

        elif page == "Verification Portal":
            driver_name = st.text_input("Enter driver")
            otp_driver = st.text_input("Enter OTP")
            submit_status = st.button("Submit")
            if submit_status:

                if otp_driver:
                    conn = connect_to_db()
                    cursor = conn.cursor()
                    cursor.execute("SELECT otp FROM generate_otp_to_owner WHERE driver_alloted = %s", (driver_name,))
                    result_otp = cursor.fetchone()  # Fetch the OTP from the query result
                    conn.close()

                    if result_otp and result_otp[0] == otp_driver:  # Check if OTP matches
                        conn = connect_to_db()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE generate_otp_to_owner SET fullfilled = %s WHERE driver_alloted = %s",
                                       (True, driver_name))
                        conn.commit()
                        conn.close()
                    else:
                        st.warning("Wrong OTP")