from web3 import Web3
from variable_validator import validate_variables
from make_trade import get_fee_quota
from make_trade import trade
import traceback
import time


def run():
    web3 = Web3(Web3.HTTPProvider(variables["http_provider_url"]))
    gas_price = web3.eth.gas_price
    gas_price_in_gwei = gas_price / 10**9
    target_gas_price = variables["target_gas_price"]
        
    if gas_price_in_gwei <= float(target_gas_price):
        fee_quota = get_fee_quota(variables)        
        if fee_quota["long_buy_amount_after_fee"] >= variables["long_least_buy_token_amount"]:
            trade(variables, fee_quota)
    else:
        print("Gas price is: ", gas_price_in_gwei)


def run_loop():
    try:
        while(True):
            run()
            time.sleep(60)
    except Exception as e:
        print("Crashed. Restart in 2 minutes")
        traceback.print_exc()
        time.sleep(120)
        run_loop()




if __name__ == '__main__':
    
    print("Validating config variables...")
    variables = validate_variables()

    fee_quota = get_fee_quota(variables)
    short_fee_amount = fee_quota["long_fee_amount"] / 10**variables["sell_token_decimals"]
    short_buy_amount_after_fee = fee_quota["long_buy_amount_after_fee"] / 10**variables["buy_token_decimals"]

    print("Current Quote: Trade {0} {1} for {2} {3} with fee {4} {5}".format(\
        variables["short_sell_token_amount"], variables["sell_token_symbol"], short_buy_amount_after_fee,\
        variables["buy_token_symbol"], short_fee_amount, variables["sell_token_symbol"]))

    print("Desired Trade: Trade {0} {1} for at least {2} {3} when gas price is lower than {4} gwei".format(\
        variables["short_sell_token_amount"], variables["sell_token_symbol"], variables["short_least_buy_token_amount"],\
        variables["buy_token_symbol"], variables["target_gas_price"]))

    input("Press Enter to confirm...")

    run_loop()


