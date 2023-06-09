import requests

from .secrets import api_key, news_api
from django.http import JsonResponse


def searchStock(symbol):
    try:
        api_key_value = api_key

        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&apikey={api_key}"

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


def searchAccount(array, account):
    start = 0
    end = len(array) - 1

    while start <= end:
        mid = (start + end) // 2
        if array[mid].account_number.lower() == account:
            return True
        elif array[mid].account_number.lower() < account:
            start = mid + 1
        else:
            end = mid - 1

    return False


def getNews(symbols):
    key = news_api
    url = f"https://api.marketaux.com/v1/news/all?exchanges=INDEXSP&filter_entities=true&limit=10&published_after=2023-06-15T00:16&api_token={key}"

    response = requests.get(url).json()
    data = []

    for item in response['data']:
        title = item['title']
        link = item['url']
        image_url = item['image_url']
        snippet = item['snippet']
        data.append({'title': title, 'link': link,
                    "image_url": image_url, 'snippet': snippet})

    return data
