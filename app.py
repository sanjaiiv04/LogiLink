import streamlit as st
from signup import signup
from dashboard import dashboard
from login import login
def main():
    if 'page' not in st.session_state or st.session_state['page'] == 'signup':
        signup()
    elif st.session_state['page'] == 'dashboard':
        role = st.session_state['role']
        dashboard(role)
    else:
        login()


if __name__ == "__main__":
    main()
