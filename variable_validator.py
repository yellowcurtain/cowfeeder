from web3 import Web3
from erc20_token import Token
import json
import sys
import os


def validate_variables():
    
    ##################################
    # 1: get config variables
    ##################################
    
    with open("config.json") as f: config = json.load(f)

    if config["network"] == "xDai":
        chain_id = "100"
        base_url = "https://protocol-xdai.gnosis.io/api/v1/"
        explorer_base_url = "https://gnosis-protocol.io/xdai/orders/"
        gp2_settlement_address = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
        gp2_vaultrelayer_address = "0xc92e8bdf79f0507f65a392b0ab4667716bfe0110"

    elif config["network"] == "mainnet":
        chain_id = "1"
        base_url = "https://protocol-mainnet.gnosis.io/api/v1/"
        explorer_base_url = "https://gnosis-protocol.io/mainnet/orders/"
        gp2_settlement_address = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
        gp2_vaultrelayer_address = "0xc92e8bdf79f0507f65a392b0ab4667716bfe0110"
        
    http_provider_url = config["http_provider_url"]
    wallet_address = config["your_wallet_address"]
    sell_token_address = config["sell_token_address"]
    short_sell_token_amount = config["sell_token_amount"]
    buy_token_address = config["buy_token_address"]
    short_least_buy_token_amount = config["least_buy_token_amount"]
    target_gas_price = config["target_gas_price"]
        
    private_key = config["private_key"]    # if not setting private key in config, search environment variable
    if private_key == "":
        private_key = os.environ.get("private_key")
    if not private_key:
        print("Private key not found")
        sys.exit()


    ##################################
    # 2: check http provider connection
    ##################################

    web3 = Web3(Web3.HTTPProvider(http_provider_url))
    is_connected = web3.isConnected()
    if is_connected == False:
        print("Failed to connect to http provider.")
        sys.exit()


    ##################################
    # 3: get token details
    ##################################

    sell_token = Token(http_provider_url, sell_token_address)
    sell_token_symbol = sell_token.symbol()
    sell_token_decimals = sell_token.decimals()
    long_sell_token_amount = float(short_sell_token_amount) * 10**sell_token_decimals
    buy_token = Token(http_provider_url, buy_token_address)
    buy_token_symbol = buy_token.symbol()
    buy_token_decimals = buy_token.decimals()
    long_least_buy_token_amount = float(short_least_buy_token_amount) * 10**buy_token_decimals


    ##################################
    # 4: check balance
    ##################################

    balance = sell_token.balance_of(wallet_address)
    if balance < long_sell_token_amount:
        print("Not enough balance.")
        sys.exit()


    ##################################
    # 5: check allowance for approve status
    ##################################

    allowance = sell_token.allowance(wallet_address, gp2_vaultrelayer_address)
    if allowance == 0:
        print("Approve cowswap to spend token.")
        sys.exit()


    variables = {
        "chain_id": chain_id,
        "base_url": base_url,
        "explorer_base_url": explorer_base_url,
        "gp2_settlement_address": gp2_settlement_address,
        "gp2_vaultrelayer_address": gp2_vaultrelayer_address,
        "http_provider_url": http_provider_url,
        "wallet_address": wallet_address,
        "private_key": private_key,
        "sell_token_address": sell_token_address,
        "sell_token_symbol": sell_token_symbol,
        "sell_token_decimals": sell_token_decimals,
        "short_sell_token_amount": short_sell_token_amount,
        "long_sell_token_amount": long_sell_token_amount,
        "buy_token_address": buy_token_address,
        "buy_token_symbol": buy_token_symbol,
        "buy_token_decimals": buy_token_decimals,
        "short_least_buy_token_amount": short_least_buy_token_amount,
        "long_least_buy_token_amount": long_least_buy_token_amount,
        "target_gas_price": target_gas_price
    }
    
    return variables





