from connectiondb import connect_to_db
import random
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import pydeck as pdk
import folium
from streamlit_folium import folium_static
import numpy as np
from connectiondb import connect_to_db

random_location = {'latitude': 13.0827, 'longitude': 80.2707}

def dashboard(role):
    st.sidebar.image("./logo.png", use_column_width=True)
    st.title(f"LogiLink {role.capitalize()} Dashboard")
    st.sidebar.title("Navigate")

    if role == 'owner':
        page = st.sidebar.radio("Select Page", ("My Info","Inhouse Driver DataBase", "My Location", "Verification Portal"))
        if page == "My Info":
            st.write("Owner's Info Page")
            name_owner=st.session_state['user']
            conn=connect_to_db()
            cursor=conn.cursor()
            driver_dtls=cursor.execute("select role,username,email,address from login_access where username= %s",(name_owner,))
            result = cursor.fetchone()
            if result:
                result = np.asanyarray(result)
                result = result.reshape(1,4)
                df=pd.DataFrame(result,columns=['Role','Name','Email','Address'])
                st.write(df)
            logout_status = st.button("Logout")
            if logout_status:
                st.session_state['page'] = None
        elif page == "Inhouse Driver DataBase":
            st.write("Inhouse Drivers DataBase")
            conn = connect_to_db()
            cursor=conn.cursor()
            driver_dtls=cursor.execute("select role,username,email,address from login_access where role=%s",("driver",))
            result = cursor.fetchall()
            if result:
                result = np.asanyarray(result)
                df=pd.DataFrame(result,columns=['Role','Name','Email','Address'])
                st.write(df)
            pkg_dtls = st.text_input("Package Name",key='package')
            driver_assign=st.text_input("Assign driver",key='assigned_driver')
            owner_current=st.session_state['user']
            submit_status=st.button("Submit")
            if submit_status:
                cursor.execute("SELECT * FROM driver_owner_verification WHERE package_details = %s", (pkg_dtls,))
                pkg_already_exists = cursor.fetchone()
                if pkg_already_exists:
                    st.warning("Package Already Exists!!!")
                else:
                    cursor.execute("INSERT INTO driver_owner_verification (owner_alloted, driver_alloted,package_details) VALUES (%s, %s, %s)", (owner_current, driver_assign, pkg_dtls))
                    st.success("Driver alloted successfully")
                    conn.commit()

        elif page == "My Location":
            try:
                location = streamlit_geolocation()
                st.write("Package Location Page")

                # Create a folium map centered at the user's location
                m = folium.Map(location=[location['latitude'], location['longitude']], zoom_start=10)

                # Add marker for user's location
                folium.Marker(
                    [location['latitude'], location['longitude']],
                    popup="Your Location",
                    icon=folium.Icon(color="blue")
                ).add_to(m)

                # Add marker for random location
                folium.Marker(
                    [random_location['latitude'], random_location['longitude']],
                    popup="Random Location",
                    icon=folium.Icon(color="red")
                ).add_to(m)

                # Add a line between the two locations
                folium.PolyLine(
                    locations=[[location['latitude'], location['longitude']],
                               [random_location['latitude'], random_location['longitude']]],
                    color='green',
                    weight=5,
                    opacity=0.7
                ).add_to(m)

                # Display the map
                folium_static(m)

                # Calculate distance
                distance = geodesic((location['latitude'], location['longitude']),
                                    (random_location['latitude'], random_location['longitude'])).miles
                st.write(f"Distance to random location: {distance:.2f} miles")

                # Estimate ETA (assuming average speed of 30 mph)
                average_speed_mph = 30
                eta_hours = distance / average_speed_mph
                current_time = datetime.now()
                eta_time = current_time + timedelta(hours=eta_hours)
                st.write(f"Estimated Time of Arrival: {eta_time.strftime('%Y-%m-%d %H:%M:%S')}")

            except Exception as e:
                st.error(f"Update Location")
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
            name_driver=st.session_state['user']
            conn=connect_to_db()
            cursor=conn.cursor()
            driver_dtls=cursor.execute("select role,username,email,address from login_access where username= %s",(name_driver,))
            result = cursor.fetchone()
            if result:
                result = np.asanyarray(result)
                result = result.reshape(1,4)
                df=pd.DataFrame(result,columns=['Role','Name','Email','Address'])
                st.write(df)
            logout_status = st.button("Logout")
            if logout_status:
                st.session_state['page'] = None
        elif page == "My Location":
            try:
                location = streamlit_geolocation()
                st.write("Package Location Page")

                # Create a folium map centered at the user's location
                m = folium.Map(location=[location['latitude'], location['longitude']], zoom_start=10)

                # Add marker for user's location
                folium.Marker(
                    [location['latitude'], location['longitude']],
                    popup="Your Location",
                    icon=folium.Icon(color="blue")
                ).add_to(m)

                # Add marker for random location
                folium.Marker(
                    [random_location['latitude'], random_location['longitude']],
                    popup="Random Location",
                    icon=folium.Icon(color="red")
                ).add_to(m)

                # Add a line between the two locations
                folium.PolyLine(
                    locations=[[location['latitude'], location['longitude']],
                               [random_location['latitude'], random_location['longitude']]],
                    color='green',
                    weight=5,
                    opacity=0.7
                ).add_to(m)

                # Display the map
                folium_static(m)

                # Calculate distance
                distance = geodesic((location['latitude'], location['longitude']),
                                    (random_location['latitude'], random_location['longitude'])).miles
                st.write(f"Distance to random location: {distance:.2f} miles")

                # Estimate ETA (assuming average speed of 30 mph)
                average_speed_mph = 30
                eta_hours = distance / average_speed_mph
                current_time = datetime.now()
                eta_time = current_time + timedelta(hours=eta_hours)
                st.write(f"Estimated Time of Arrival: {eta_time.strftime('%Y-%m-%d %H:%M:%S')}")

            except Exception as e:
                st.error(f"Update Location")
        elif page == "Request OTP":
            st.write("Driver's OTP Request Page")
            username_otp = st.session_state['user']
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
            driver_name = st.session_state['user']
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
                        st.success("OTP Verification Successful")
                    else:
                        st.warning("Wrong OTP")
