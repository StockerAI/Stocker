from yahoo_fin import stock_info
import pandas as pd

def stock_parser(tickers):
    base_data_frame = pd.DataFrame(columns=['tickerId', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume'])
    for ticker in tickers:
        # TODO: Check dataframe and validate the missing tickers.
        try:
            current_data_frame = stock_info.get_data(ticker[2], index_as_date = False)
            current_data_frame['tickerId'] = ticker[0]
            current_data_frame.drop('ticker', axis=1, inplace=True)
            base_data_frame = pd.concat([base_data_frame, current_data_frame], axis=0)
        except:
            print('There were no stock info data for ticker:', ticker)
    base_data_frame.reset_index(drop=True, inplace=True)
    base_data_frame.index.rename('stockId', inplace=True)
    base_data_frame.dropna(inplace=True)
    base_list = base_data_frame.to_dict('records')
    return base_list
