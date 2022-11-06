import itertools
from yahoo_fin import stock_info
from tqdm import tqdm
import time
import modin.pandas as pd
from pprint import pprint
from Control.Util_Controllers.modin_utils import on_demand_garbage_collect

def stock_parser_bak2(tickers):
    tickers_tmp = tickers[:200]
    base_data_frame = pd.DataFrame(columns=['tickerId', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume'])
    for ticker in tqdm(tickers_tmp, desc='Parsing Stock Data', unit=' ticker', total=len(tickers_tmp)): # 13121
        try:
            current_data_frame = stock_info.get_data(ticker[2], index_as_date = False)
            current_data_frame['tickerId'] = ticker[0]
            current_data_frame.drop('ticker', axis=1, inplace=True)
            base_data_frame = pd.concat([base_data_frame, current_data_frame], axis=0)
        except Exception as e:
            print(f'[Exception {e}] There were no stock info data for ticker:', ticker)
    base_data_frame.reset_index(drop=True, inplace=True)
    base_data_frame.index.rename('stockId', inplace=True)
    base_data_frame.dropna(inplace=True)
    pprint(base_data_frame)
    # base_list = base_data_frame.to_dict('records')
    # return base_list


def stock_parser_worker(ticker, curr_idx, df_index_ptr):
    base_data_frame = pd.DataFrame(columns=['tickerId', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume'])
    e_flag = False
    try:
        current_data_frame = stock_info.get_data(ticker[2], index_as_date=False)
    except Exception as e:
        e_flag = True
        print(f'[Exception {e}] There were no stock info data for ticker:', ticker)
    # This means that all exceptions occur in the try block
    if not e_flag:
        current_data_frame['tickerId'] = ticker[0]
        current_data_frame.drop('ticker', axis=1, inplace=True)
        base_data_frame = pd.concat([base_data_frame, current_data_frame], axis=0)

    base_data_frame.dropna(inplace=True)
    base_data_frame.index = range(df_index_ptr, df_index_ptr + base_data_frame.shape[0])
    base_data_frame.index.rename('stockId', inplace=True)
    on_demand_garbage_collect()
    pprint(base_data_frame)
    base_list = base_data_frame.to_dict('records')
    return base_list, curr_idx + 1, df_index_ptr + base_data_frame.shape[0]


def stock_parser(tickers):
    tickers_tmp = tickers[:200]
    curr_idx, df_index_ptr = 0, 0
    for ticker in tqdm(tickers_tmp, desc='Parsing Stock Data', unit=' ticker', total=len(tickers_tmp)):
        base_list, curr_idx, df_index_ptr = stock_parser_worker(ticker, curr_idx, df_index_ptr)
        # time.sleep(1)
    # TODO: insert into database


def stock_parser_bak(tickers):
    prev_num_elements = 0
    curr_num_elements = 0
    tickers_tmp = itertools.islice(tickers, 0, 10)
    base_data_frame = pd.DataFrame(columns=['tickerId', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume'])
    for ticker in tqdm(tickers_tmp, desc='Parsing Stock Data', unit=' ticker', total=10):
        '''
        (1, 'DOW', 'AAPL', None)
        (2, 'DOW', 'AMGN', None)
        (3, 'DOW', 'AXP', None)
        '''
        try:
            current_data_frame = stock_info.get_data(ticker[2], index_as_date = False)
            current_data_frame['tickerId'] = ticker[0]
            current_data_frame.drop('ticker', axis=1, inplace=True)
            # get number of elements in current_data_frame
            curr_num_elements += current_data_frame.shape[0]
            # get index of current_data_frame

            # current_data_frame.reset_index(drop=True, inplace=True)
            # current_data_frame.index.rename('stockId', inplace=True)
            base_data_frame = pd.concat([base_data_frame, current_data_frame], axis=0)
        except:
            print('There were no stock info data for ticker:', ticker)
    base_data_frame.dropna(inplace=True)
    base_list = base_data_frame.to_dict('records')
    pprint(base_data_frame)



'''
try:
    current_data_frame = stock_info.get_data(ticker[2], index_as_date = False)
    current_data_frame['tickerId'] = ticker[0]
    current_data_frame.drop('ticker', axis=1, inplace=True)
    current_data_frame.reset_index(drop=True, inplace=True)
    current_data_frame.index.rename('stockId', inplace=True)
    current_data_frame.dropna(inplace=True)
    base_list = current_data_frame.to_dict('records')
    yield base_list
except:
    print('There were no stock info data for ticker:', ticker)
'''

