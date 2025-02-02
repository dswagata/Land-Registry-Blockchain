from web3 import Web3
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not web3.is_connected():
    raise Exception("Web3 is not connected. Ensure Ganache is running.")

# Load Contract ABI and Address from build/contracts/LandRegistry.json
with open("build/contracts/LandRegistry.json") as f:
    contract_data = json.load(f)

contract_abi = contract_data["abi"]
contract_address = contract_data["networks"]["5777"]["address"]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Register a new land parcel
def register_land(account, land_id, location, area):
    try:
        tx_hash = contract.functions.registerLand(
            int(land_id), location, int(area)
        ).transact({'from': account, 'gas': 500000})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return f"Land registered successfully! Tx: {tx_hash.hex()}"
    except Exception as e:
        return f"Error: {str(e)}"

# Transfer ownership of a land parcel
def transfer_ownership(account, land_id, new_owner):
    try:
        tx_hash = contract.functions.transferOwnership(
            int(land_id), new_owner
        ).transact({'from': account, 'gas': 500000})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return f"Ownership transferred! Tx: {tx_hash.hex()}"
    except Exception as e:
        return f"Error: {str(e)}"

# Fetch land details
def get_land_details(land_id):
    try:
        land = contract.functions.getLand(int(land_id)).call()
        return {
            "ID": land[0],
            "Location": land[1],
            "Area": land[2],
            "Owner": land[3],
            "Registered": land[4]
        }
    except Exception as e:
        return {"Error": str(e)}

# Check if a land parcel is registered
def is_land_registered(land_id):
    try:
        return contract.functions.isLandRegistered(int(land_id)).call()
    except Exception as e:
        return f"Error: {str(e)}"
