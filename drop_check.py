import re

import requests
from prettytable import PrettyTable


def read_file():
    with open(".env", 'r') as file:
        data = [line.strip() for line in file if not line.startswith("#")]
    return data


def get_drop_data(wallet_address) -> dict:
    response = None
    result_dict = []
    url = "https://airdrop.altlayer.io/"

    payload = f'["{wallet_address}"]'
    headers = {
        'content-type': 'text/plain;charset=UTF-8',
        'next-action': '6817e8f24aae7e8aed1d5226e9b368ab8c1ded5d'
    }
    response_code = 0
    while response_code != 200:
        response = requests.request("POST", url, headers=headers, data=payload)
        response_code = response.status_code

    # Extracting information using regular expressions
    pattern = re.compile(
        r'address\":\"(?P<address>0x\w+)\",\"amount\":\"(?P<amount>\d+)\".+,'
        r'"og":(?P<og>\w+),"ottie":(?P<ottie>\w+),"altitude":(?P<altitude>\w+),'
        r'"eigenRestaker":(?P<eigenRestaker>\w+),"eigenEcosystem":(?P<eigenEcosystem>\w+)}')

    match = pattern.search(response.text)

    if match:
        result_dict = match.groupdict()
        result_dict["amount"] = int(result_dict["amount"])/1000000000000000000
    else:
        result_dict = {
            "address": wallet_address,
            "amount": 0,
            "og": False,
            "ottie": False,
            "altitude": False,
            "eigenRestaker": False,
            "eigenEcosystem": False
        }

    return result_dict


credits = []
wallet_addresses = read_file()
progress = 0
progress_delta = 100 / len(wallet_addresses)
print(f"Current progress - {progress}%")
for address in wallet_addresses:
    credits.append(get_drop_data(address))
    progress += progress_delta
    print(f"Current progress - {round(progress, 2)}%")

sorted_credits = sorted(credits, key=lambda d: d['amount'], reverse=True)

table = PrettyTable(['address', 'amount', 'og', 'ottie', 'altitude', 'eigenRestaker', 'eigenEcosystem'])
table.align = "l"

for credit in sorted_credits:
    table.add_row([credit.get("address"), credit.get("amount"), credit.get("og"), credit.get("ottie"),
                   credit.get("altitude"), credit.get("eigenRestaker"), credit.get("eigenEcosystem")])
print(table)
