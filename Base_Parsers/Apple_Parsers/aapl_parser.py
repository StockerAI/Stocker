from yahoo_fin import stock_info

apple_daily = stock_info.get_data("aapl", interval="1d")

def add_daily_result(row):
    '''
    Function that returns '1' or '0' depending
    on the result of the 'close' and 'open' values.
    '''
    if row['close'] > row['open']:
        return 1
    else:
        return 0

apple_daily['result'] = apple_daily.apply(lambda row: add_daily_result(row), axis=1)

apple_daily = apple_daily.fillna(0)

print(apple_daily)

