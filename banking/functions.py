def get_stocks():
    api_key = "xxxxxxxx"
    # Test stocks
    list_stocks = ["AAPL", "AM", "MSFT", "CGC", "MTTR", "OGI"]
    url = f"https://api.twelvedata.com/time_series?symbol={','.join(list_stocks)}&apikey={api_key}&interval=2h"
    response = requests.get(url).json()
    stocks_data = []

    # For each ticker, get that object and it's value from the response add new object to array, return array
    for ticker in list_stocks:
        stock_values = response.get(ticker, {}).get('values', [])
        if stock_values:
            latest_price = stock_values[0].get('close', '')
            stocks_data.append({'ticker': ticker, 'price': latest_price})
    return print({'stocks_data': stocks_data})
