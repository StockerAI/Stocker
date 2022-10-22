from yahoo_fin import stock_info

amazon_daily = stock_info.get_data("amzn", interval="1d")

def add_daily_result(row):
    '''
    Function that returns '1' or '0' depending
    on the result of the 'close' and 'open' values.
    '''
    if row['close'] > row['open']:
        return 1
    else:
        return 0

amazon_daily['result'] = amazon_daily.apply(lambda row: add_daily_result(row), axis=1)

amazon_daily = amazon_daily.fillna(0)

print(amazon_daily)