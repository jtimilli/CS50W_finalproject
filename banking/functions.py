import requests

from .secrets import api_key
from django.http import JsonResponse


def searchStock(symbol):
    try:
        api_key_value = api_key

        # Call API
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&apikey={api_key}"

        #
        response = requests.get(url).json()
        data = response['meta']

        if response.get("status") == 'ok':
            stock = {}
            latest_price = '%.2f' % float(response["values"][0]["close"])
            stock["currency"] = data["currency"]
            stock["price"] = latest_price
            stock["symbol"] = data["symbol"]
            stock["type"] = data["type"]
            stock["exchange"] = data["exchange"]
            return {"status": 200, "data": stock}
        elif response.get("code") == 400:
            return {"status": 400, "error": "No symbol with that ticker try again"}
    except Exception as e:
        return {"status": 500, "error": str(e)}
