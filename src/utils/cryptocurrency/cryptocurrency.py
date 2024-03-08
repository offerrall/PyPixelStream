import requests

def get_cripto_list() -> list[tuple[str, str]]:
    """
    List of criptocurrencies with their symbol, feel free to add more criptocurrencies
    """
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

def get_fiat_list() -> list[str]:
    """
    List of fiat currencies, feel free to add more fiat currencies
    """
    fiat_list = [
        "eur",
        "usd"
    ]

    return fiat_list

def get_only_name_list() -> list[str]:
    """
    Get only the name of the criptocurrencies from the list, useful for the dropdown menu
    """
    cripts_list = get_cripto_list()
    only_name_list = []
    for cripto in cripts_list:
        only_name_list.append(cripto[0])
    
    return only_name_list

def cripto_to_symbol(cripto_name: str) -> str:
    """
    Get the symbol of the criptocurrency from the name
    """
    cripts_list = get_cripto_list()
    for cripto in cripts_list:
        if cripto[0] == cripto_name:
            return cripto[1]
    
    return None

def get_cripto_price(cripto_name: str, fiat: str = "eur") -> float:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto_name}&vs_currencies={fiat}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[cripto_name][fiat]
    
    raise Exception("Error with the request")