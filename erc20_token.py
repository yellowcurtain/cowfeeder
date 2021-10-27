from web3 import Web3
import json

class Token(object):
    
    def __init__(self, http_provider_url, address, abi_path="abis/ERC20.json"):
        self.http_provider_url = http_provider_url
        self.address = Web3.toChecksumAddress(address)
        with open(abi_path) as f: abi = json.load(f)
        self.abi = abi
        web3 = Web3(Web3.HTTPProvider(http_provider_url))
        self.contract = web3.eth.contract(address=self.address, abi=abi)

    def balance_of(self, address):
        checksum_address = Web3.toChecksumAddress(address)
        balance = self.contract.functions.balanceOf(checksum_address).call()
        return balance
    
    def decimals(self):
        decimals = self.contract.functions.decimals().call()
        return decimals
        
    def readable_balance_of(self, address):
        checksum_address = Web3.toChecksumAddress(address)
        balance = self.contract.functions.balanceOf(checksum_address).call()
        decimals = self.contract.functions.decimals().call()
        readable_balance = balance / 10**decimals
        return readable_balance
        
    def symbol(self):
        symbol = self.contract.functions.symbol().call()
        return symbol
        
    def name(self):
        name = self.contract.functions.name().call()
        return name
        
    def allowance(self, owner, spender):
        owner = Web3.toChecksumAddress(owner)
        spender = Web3.toChecksumAddress(spender)
        allowance = self.contract.functions.allowance(owner, spender).call()
        return allowance
    
    def allowance(self, owner, spender):
        owner = Web3.toChecksumAddress(owner)
        spender = Web3.toChecksumAddress(spender)
        allowance = self.contract.functions.allowance(owner, spender).call()
        return allowance
        
    def approve(self, spender, value):
        spender = Web3.toChecksumAddress(spender)
        is_approved = self.contract.functions.approve(owner, spender, value).call()
        return is_approved

    def approve_all(self, spender):
        value = 115792089237316195423570985008687907853269984665640564039457584007913129639935
        spender = Web3.toChecksumAddress(spender)
        is_approved = self.contract.functions.approve(owner, spender, value).call()
        return is_approved


