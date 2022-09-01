import requests


def get_current_funding_rates():
    url = 'https://fapi.coinglass.com/api/fundingRate/v2/home'
    response = requests.get(url)

    data_dict = dict()

    if response.status_code == 200:
        data = response.json()['data']
        for element in data:
            symbol = element['symbol'] + 'USDT'
            exchange = [k for k in element['uMarginList'] if (k['exchangeName'] == 'Bybit' and k['status'] == 2)]
            if len(exchange) > 0:
                info = exchange[0]
                data_dict[symbol] = {
                    'current_rate': info['rate']
                }
        return data_dict





