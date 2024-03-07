import requests

def get_cripto_list():

    cripts_list = [
        ("bitcoin", "btc"),
        ("ethereum", "eth"),
        ("cardano", "ada"),
        ("binancecoin", "bnb"),
        ("tether", "usdt"),
        ("ripple", "xrp"),
        ("solana", "sol"),
        ("dogecoin", "doge"),
        ("polkadot", "dot")
    ]

    return cripts_list

def get_fiat_list():
    fiat_list = [
        "eur",
        "usd"
    ]

    return fiat_list

def get_only_name_list():
    cripts_list = get_cripto_list()
    only_name_list = []
    for cripto in cripts_list:
        only_name_list.append(cripto[0])
    
    return only_name_list

def cripto_to_symbol(cripto_name: str):
    cripts_list = get_cripto_list()
    for cripto in cripts_list:
        if cripto[0] == cripto_name:
            return cripto[1]
    
    return None

def get_cripto_price(cripto_name: str, fiat: str = "eur"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto_name}&vs_currencies={fiat}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[cripto_name][fiat]
    
    raise Exception("Error with the request")