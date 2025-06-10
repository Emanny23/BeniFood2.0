
import streamlit as st
import pandas as pd
import os
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

st.set_page_config(page_title="Stored Files", page_icon="📂", layout="wide")

# --- RE-INITIALIZE AUTHENTICATOR FOR LOGOUT BUTTON ---
# This is necessary to make authenticator methods available on this page
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookies']['name'],
    config['cookies']['key'],
    config['cookies']['expiry_days']
)

# --- RETRIEVE AUTHENTICATION STATUS FROM SESSION STATE ---
authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

# --- MAIN APP LOGIC ---
if authentication_status:
    # THE FIX: Add the logout button and welcome message to this page as well
    authenticator.logout(location='sidebar')
    st.sidebar.title(f"Welcome *{name}*")
    
    st.title(f"📂 Stored Files")
    st.markdown("Here you can view and manage all of your data files.")

    user_data_dir = f"data/{username}"
    if not os.path.exists(user_data_dir):
        st.info("No data directory found. Go to the Data Entry page to create your first file.")
        st.stop()
        
    files = [f for f in os.listdir(user_data_dir) if f.endswith('.csv')]

    if not files:
        st.warning("You have not created any data files yet.")
    else:
        for file_name in sorted(files):
            file_path = os.path.join(user_data_dir, file_name)
            
            with st.expander(f"**{file_name}**"):
                try:
                    df = pd.read_csv(file_path)
                    st.dataframe(df, use_container_width=True)
                    
                    if st.button(f"Delete `{file_name}`", key=f"del_{file_name}", type="primary"):
                        os.remove(file_path)
                        st.success(f"`{file_name}` has been deleted.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Could not read or process file {file_name}. Error: {e}")

else:
    st.warning("You are not logged in. Please go to the main page to log in or create an account.")