from web3 import Web3
import os

infura_key = os.environ.get("INFURA_KEY")

w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/" + infura_key))
if w3.isConnected():
    account = w3.eth.account.create()
    private_key = account.privateKey.hex()
    address = account.address
    print(private_key)
    print(address)
else:
    raise Exception("Connection Failed")
