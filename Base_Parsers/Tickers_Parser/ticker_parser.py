from yahoo_fin import stock_info

ticker_values = {
    'DOW': stock_info.tickers_dow(),
    # 'FTSE_100': stock_info.tickers_ftse100(),
    # 'FTSE_250': stock_info.tickers_ftse250(),
    'IBOVESPA': stock_info.tickers_ibovespa(),
    'NASDAQ': stock_info.tickers_nasdaq(),
    'NIFTY50': stock_info.tickers_nifty50(),
    'NIFTYBANK': stock_info.tickers_niftybank(),
    'OTHER': stock_info.tickers_other(),
    'SP500': stock_info.tickers_sp500()
}

ticker_value_list = list()

for stock, ticker_list in ticker_values.items():
    for ticker in ticker_list:
        ticker_value_list.append({'stockMarket': stock, 'tickerName': ticker})
