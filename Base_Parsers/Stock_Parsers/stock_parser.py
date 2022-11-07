
import modin.pandas as pd
from yahoo_fin import stock_info
from Control.Util_Controllers.modin_utils import on_demand_garbage_collect

def stock_parser_worker(ticker, curr_idx, df_index_ptr):
    base_data_frame = pd.DataFrame(columns=['tickerId', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume'])
    e_flag = False
    try:
        current_data_frame = stock_info.get_data(ticker[2], index_as_date=False)
    except Exception as e:
        e_flag = True
    if not e_flag:
        current_data_frame['tickerId'] = ticker[0]
        current_data_frame.drop('ticker', axis=1, inplace=True)
        base_data_frame = pd.concat([base_data_frame, current_data_frame], axis=0)

    base_data_frame.dropna(inplace=True)
    base_data_frame.index = range(df_index_ptr, df_index_ptr + base_data_frame.shape[0])
    base_data_frame.index.rename('stockId', inplace=True)
    base_list = base_data_frame.to_dict('records')
    on_demand_garbage_collect()
    return base_list, curr_idx + 1, df_index_ptr + base_data_frame.shape[0]

def stock_parser(ticker):
    curr_idx, df_index_ptr = 0, 0
    base_list, curr_idx, df_index_ptr = stock_parser_worker(ticker, curr_idx, df_index_ptr)
    # check if base_list is empty
    if base_list:
        return base_list
