import streamlit as st
import pandas as pd
from datetime import date
import os
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

# --- PAGE CONFIG ---
st.set_page_config(page_title="Beni Food Data Entry", page_icon="🛒", layout="wide")

# --- USER AUTHENTICATION ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookies']['name'],
    config['cookies']['key'],
    config['cookies']['expiry_days']
)

# --- LOGIN & REGISTRATION ---
login_col, _, register_col = st.columns([2, 1, 2])

with login_col:
    st.subheader("Login to your Account")
    authenticator.login(location='main')

with register_col:
    st.subheader("Create a New Account")
    try:
        # THE FIX: The 'pre_authorized' parameter has been completely removed
        # to allow anyone to register.
        if authenticator.register_user(location='main'):
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success('User registered successfully! You can now log in.')
    except Exception as e:
        st.error(e)

# Retrieve authentication status from st.session_state
authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

# --- MAIN APP LOGIC ---
if authentication_status:
    user_data_dir = f"data/{username}"
    os.makedirs(user_data_dir, exist_ok=True)

    # --- HEADER ---
    authenticator.logout(location='sidebar')
    st.sidebar.title(f"Welcome *{name}*")
    
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFhr55yxJMuR5NASWcA92yZwSTLJQFQeXtxg&s", width=100)
    st.title("🛒 Beni Food Data Entry")
    st.markdown("Select a file to add data to, or create a new one.")

    # --- FILE MANAGEMENT ---
    files = [f for f in os.listdir(user_data_dir) if f.endswith('.csv')]
    file_options = ["<Create New File>"] + files
    selected_file = st.selectbox("Select a Data File", options=file_options)
    
    data_file_path = None
    if selected_file == "<Create New File>":
        new_file_name = st.text_input("Enter new file name (e.g., 'January_Sales.csv')")
        if new_file_name:
            if not new_file_name.endswith('.csv'):
                new_file_name += '.csv'
            data_file_path = os.path.join(user_data_dir, new_file_name)
    else:
        data_file_path = os.path.join(user_data_dir, selected_file)

    if data_file_path:
        if not os.path.exists(data_file_path):
            df_init = pd.DataFrame(columns=["Date", "Department", "Item", "Sale Amount"])
            df_init.to_csv(data_file_path, index=False)
            st.success(f"Created new file: `{os.path.basename(data_file_path)}`")

        st.subheader(f"📝 Add Entry to `{os.path.basename(data_file_path)}`")
        with st.form("data_entry_form", clear_on_submit=True):
            entry_date = st.date_input("Date", value=date.today())
            department = st.selectbox("Department", ["General Food", "Meat/Fish", "Drinks", "Service Fees", "Snacks", "Cleaning&Body", "Pinless Recharge", "Household", "Condiment", "Clothes", "Frozen", "Pasta/Rice", "Misc.", "Vitmains/Medicine", "Hygiene Feminine", "Calling Card", "Tobacco", "Cleaning", "Dairy", "Grocery Non-Taxable"])
            item = st.text_input("Item Name")
            sale_amount = st.number_input("Sale Amount ($)", min_value=0.0, step=0.01, format="%.2f")
            submitted = st.form_submit_button("Submit Entry")

            if submitted:
                if item.strip() == "":
                    st.warning("Please enter a valid item name.")
                else:
                    existing_data = pd.read_csv(data_file_path)
                    new_row = {"Date": entry_date, "Department": department, "Item": item.strip(), "Sale Amount": sale_amount}
                    updated_data = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)
                    updated_data.to_csv(data_file_path, index=False)
                    st.success("Data submitted successfully!")

        st.divider()
        st.subheader(f"📊 Data in `{os.path.basename(data_file_path)}`")
        if st.button(f"🗑️ Delete this file ({os.path.basename(data_file_path)})", type="primary"):
            os.remove(data_file_path)
            st.rerun()

        try:
            data = pd.read_csv(data_file_path)
            st.dataframe(data, use_container_width=True)
        except FileNotFoundError:
            st.info("File has been deleted. Please select or create another file.")


elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.info("Please log in or create an account to get started.")





# import streamlit as st
# import pandas as pd
# from datetime import date
# import os

# # File to store data
# DATA_FILE = "Benifood_data.csv"

# # Initialize data file if not exists
# if not os.path.exists(DATA_FILE):
#     df_init = pd.DataFrame(columns=["Date", "Department", "Item", "Sale Amount"])
#     df_init.to_csv(DATA_FILE, index=False)

# # App Title

# st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFhr55yxJMuR5NASWcA92yZwSTLJQFQeXtxg&s")
# st.title("🛒 Beni Food Data Entry")

# st.markdown("Fill in the form below to record a sale.")

# # Form for data entry
# with st.form("data_entry_form"):
#     entry_date = st.date_input("Date", value=date.today())
#     department = st.selectbox("Department", ["General Food", "Meat/Fish", "Drinks", "Service Fees", "Snacks", "Cleaning&Body",
# "Pinless Recharge", "Household", "Condiment", "Clothes", "Frozen", "Pasta/Rice", "Misc.", "Vitmains/Medicine", "Hygiene Feminine",
#  "Calling Card", "Tobacco", "Cleaning", "Dairy", "Grocery Non-Taxable"])
#     item = st.text_input("Item Name")
#     sale_amount = st.number_input("Sale Amount ($)", min_value=0.0, step=0.01, format="%.2f")
    
#     submitted = st.form_submit_button("Submit")

#     if submitted:
#         if item.strip() == "":
#             st.warning("Please enter a valid item name.")
#         else:
#             # Load existing data
#             existing_data = pd.read_csv(DATA_FILE)

#             # Add new row
#             new_row = {
#                 "Date": entry_date,
#                 "Department": department,
#                 "Item": item.strip(),
#                 "Sale Amount": sale_amount
#             }
#             updated_data = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)

#             # Save updated data
#             updated_data.to_csv(DATA_FILE, index=False)
#             st.success("Data submitted successfully!")

# # Show existing data
# st.subheader("📊 Submitted Entries")
# data = pd.read_csv(DATA_FILE)
# st.dataframe(data)