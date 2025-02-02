import streamlit as st
from web3 import Web3
import backend  # Import backend functions

# Connect to Ethereum (Ganache)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Ensure Web3 connection
if not web3.is_connected():
    st.error("Web3 is not connected. Ensure Ganache is running.")
    st.stop()

# Streamlit UI
st.title("🏡 Blockchain Land Registry")

# Select Ethereum account
accounts = web3.eth.accounts
if not accounts:
    st.error("No Ethereum accounts found! Ensure Ganache is running.")
    st.stop()
else:
    selected_account = st.selectbox("Select Your Ethereum Account", accounts)

# Register Land
st.subheader("Register New Land")
land_id = st.number_input("Land ID", min_value=1, step=1)
location = st.text_input("Land Location")
area = st.number_input("Area (sq. meters)", min_value=1, step=1)

if st.button("Register Land"):
    result = backend.register_land(selected_account, land_id, location, area)
    if "Error" in result:
        st.error(result)
    else:
        st.success(result)

# Transfer Ownership
st.subheader("Transfer Land Ownership")
land_id_transfer = st.number_input("Land ID to Transfer", min_value=1, step=1)
new_owner = st.selectbox("Select New Owner", accounts)

if st.button("Transfer Ownership"):
    result = backend.transfer_ownership(selected_account, land_id_transfer, new_owner)
    if "Error" in result:
        st.error(result)
    else:
        st.success(result)

# View Land Details
st.subheader("View Land Details")
land_id_view = st.number_input("Enter Land ID to View", min_value=1, step=1)

if st.button("Fetch Details"):
    details = backend.get_land_details(land_id_view)
    if "Error" in details:
        st.error(details["Error"])
    elif details["Registered"]:
        st.write(f"**Land ID:** {details['ID']}")
        st.write(f"**Location:** {details['Location']}")
        st.write(f"**Area:** {details['Area']} sqm")
        st.write(f"**Owner:** {details['Owner']}")
    else:
        st.warning("Land not registered.")

st.sidebar.info("Connected to Ethereum Blockchain (Ganache)")