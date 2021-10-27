from eth_account.messages import encode_defunct
from eip712_structs import make_domain
from eip712_structs import Address, Boolean, Bytes, String, Uint
from eip712_structs import EIP712Struct
from hexbytes import HexBytes
from web3 import Web3
from web3.auto import w3

import requests
import json
import time
import sys


class Order(EIP712Struct):
    sellToken = Address()
    buyToken = Address()
    receiver = Address()
    sellAmount = Uint(256)
    buyAmount = Uint(256)
    validTo = Uint(32)
    appData = Bytes(32)
    feeAmount = Uint(256)
    kind = String()
    partiallyFillable = Boolean()
    sellTokenBalance = String()
    buyTokenBalance = String()


def get_fee_quota(variables):
    base_url = variables["base_url"]
    sell_token_address = variables["sell_token_address"]
    buy_token_address = variables["buy_token_address"]
    long_sell_token_amount = variables["long_sell_token_amount"]

    fee_quota = requests.get(base_url +  "feeAndQuote/sell?sellToken=" + sell_token_address +  "&buyToken=" + buy_token_address + "&sellAmountBeforeFee=" + str(int(long_sell_token_amount)))
    long_fee_amount = int(fee_quota.json()["fee"]["amount"])
    long_buy_amount_after_fee = int(fee_quota.json()["buyAmountAfterFee"])
    fee_quota = {
        "long_fee_amount": long_fee_amount,
        "long_buy_amount_after_fee": long_buy_amount_after_fee
    }
    return fee_quota

           
def place_order(variables, order):
    
    base_url = variables["base_url"]
    chain_id = variables["chain_id"]
    gp2_settlement_address = variables["gp2_settlement_address"]
    private_key = variables["private_key"]
    wallet_address = variables["wallet_address"]
    explorer_base_url = variables["explorer_base_url"]

    domain = make_domain(name='Gnosis Protocol', version='v2', chainId=chain_id, verifyingContract=gp2_settlement_address)
    my_bytes = order.signable_bytes(domain)
    hash = Web3.keccak(my_bytes)
    message = encode_defunct(primitive=hash)
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)

    request_str = '''{
      "sellToken": "''' + str(order["sellToken"]) + '''",
      "buyToken": "''' + str(order["buyToken"]) + '''",
      "receiver": "''' + str(order["receiver"]) + '''",
      "sellAmount": "''' + str(order["sellAmount"]) + '''",
      "buyAmount": "''' + str(order["buyAmount"]) + '''",
      "validTo": ''' + str(order["validTo"]) + ''',
      "appData": "''' + str(order["appData"].hex()) + '''",
      "feeAmount": "''' + str(order["feeAmount"]) + '''",
      "kind": "''' + str(order["kind"]) + '''",
      "partiallyFillable": ''' + str(order["partiallyFillable"]).lower() + ''',
      "signature": "''' + str(signed_message.signature.hex()) + '''",
      "signingScheme": "ethsign",
      "sellTokenBalance": "''' + str(order["sellTokenBalance"]) +'''",
      "buyTokenBalance": "''' + str(order["buyTokenBalance"]) +'''",
      "from": "''' + wallet_address + '''"
    }'''

    print(request_str)
    request_json = json.loads(request_str)    
    response = requests.post(base_url + "orders", json=request_json)
    print("Place order response status code: ", response.status_code)

    if response.status_code == 201:
        order_id = response.json()
        order_detail_url = explorer_base_url + order_id
        print("Order placed: ", order_detail_url)
    else:
        print("Failed to place order.")
        print(response)
    sys.exit()


    
def trade(variables, fee_quota):
    
    order = Order()
    order["kind"] = "sell"
    order["sellToken"] = variables["sell_token_address"]
    order["buyToken"] = variables["buy_token_address"]
    order["sellAmount"] = int(variables["long_sell_token_amount"]) # server only accept int type
    order["buyAmount"] = int(fee_quota["long_buy_amount_after_fee"])
    order["feeAmount"] = int(fee_quota["long_fee_amount"])
    order["receiver"] = variables["wallet_address"]
    order["validTo"] = int(time.time()) + 600
    order["appData"] = HexBytes("0x0000000000000000000000000000000000000000000000000000000000000ccc")    
    order["partiallyFillable"] = False
    order["sellTokenBalance"] = "erc20"
    order["buyTokenBalance"] = "erc20"
    
    place_order(variables, order)
  
  
  
  
  
  