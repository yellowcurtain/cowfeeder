# Cow Feeder

Cow Feeder is a bot automatically execute trade on cowswap, includes functions:
  - Monitoring Ethereum network gas price and execute trade when gas price is low and reaches target gas price set by user.
  - Protect trade from quick price change when bot waits for a good gas price.
  - Automatically approve to trade on cowswap when gas price is low and reaches target gas price set by user. (In progress)
 
Extra bonus to use Cow Feeder:
  - More chances to have CoWs. People are more likely to set same target gas price, such as 40 gwei, thus executing trade at a small time window together.

## Requirements

Python 3  


## Setup

### 1. Install dependencies
 
```bash
pip install -r requirements.txt
```

### 2. Set config.json file


```bash
{
  "network": "mainnet",
  "http_provider_url": "https://mainnet.infura.io/v3/<api-key>",
  "your_wallet_address": "0x..........",
  "private_key": "your_wallet_address_private_key",
  "sell_token_address": "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83",
  "buy_token_address": "0x4ecaba5870353805a9f068101a40e0f32ed605c6",
  "sell_token_amount": "100",
  "least_buy_token_amount": "80",
  "target_gas_price": "40"
}
```

#### Http Provider Url

```http_provider_url```: If you don't already have a http provider, you can register a free one at infura.io.

#### Private Key

```private_key```: Private key is not mnemonic. With metamask, you can find it by clicking three dots, opening account detail and exporting private key.  Private key is important. You can also leave private_key as an empty string in config.json and set it as environment variable with ```export private_key=your_wallet_private_key```. Cow Feeder handles both cases.

#### Least buy token amount

```least_buy_token_amount```: While gas price goes down, price of trading pair might change as well. If the amount of token you are getting is lower than least buy token amount, Cow Feeder will not execute trade.

#### Gas Price

```target_gas_price```: Gas price is in gwei, you can decide target gas price by referring historical gas price at etherscan.io/gastracker.



### 3. Try it on xDai network

```bash
{
  "network": "xDai",
  "http_provider_url": "https://rpc.xdaichain.com/",
  "your_wallet_address": "0x..........",
  "private_key": "your_wallet_address_private_key",
  "sell_token_address": "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83",
  "buy_token_address": "0x4ecaba5870353805a9f068101a40e0f32ed605c6",
  "sell_token_amount": "0.5",
  "least_buy_token_amount": "0.49",
  "target_gas_price": "1"
}
```

You can try it out on xDai network. You don't need a http provider api key for xDai network. Gas price on xDai network is usually at 1, you can refer to [xdai gas price oracle](https://blockscout.com/xdai/mainnet/api/v1/gas-price-oracle)


### 4. Run it

```bash
python cowfeeder.py
```




## Contributors

- Curtain (yellowcurtain3@gmail.com)



## Disclaimer
This is alpha release. Use at your own risk.



