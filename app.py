import streamlit as st
import pandas as pd
from datetime import date
import os

# File to store data
DATA_FILE = "Benifood_data.csv"

# Initialize data file if not exists
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Date", "Department", "Item", "Sale Amount"])
    df_init.to_csv(DATA_FILE, index=False)

# App Title

st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFhr55yxJMuR5NASWcA92yZwSTLJQFQeXtxg&s")
st.title("🛒 Beni Food Data Entry")

st.markdown("Fill in the form below to record a sale.")

# Form for data entry
with st.form("data_entry_form"):
    entry_date = st.date_input("Date", value=date.today())
    department = st.selectbox("Department", ["General Food", "Meat/Fish", "Drinks", "Service Fees", "Snacks", "Cleaning&Body",
"Pinless Recharge", "Household", "Condiment", "Clothes", "Frozen", "Pasta/Rice", "Misc.", "Vitmains/Medicine", "Hygiene Feminine",
 "Calling Card", "Tobacco", "Cleaning", "Dairy", "Grocery Non-Taxable"])
    item = st.text_input("Item Name")
    sale_amount = st.number_input("Sale Amount ($)", min_value=0.0, step=0.01, format="%.2f")
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        if item.strip() == "":
            st.warning("Please enter a valid item name.")
        else:
            # Load existing data
            existing_data = pd.read_csv(DATA_FILE)

            # Add new row
            new_row = {
                "Date": entry_date,
                "Department": department,
                "Item": item.strip(),
                "Sale Amount": sale_amount
            }
            updated_data = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)

            # Save updated data
            updated_data.to_csv(DATA_FILE, index=False)
            st.success("Data submitted successfully!")

# Show existing data
st.subheader("📊 Submitted Entries")
data = pd.read_csv(DATA_FILE)
st.dataframe(data)