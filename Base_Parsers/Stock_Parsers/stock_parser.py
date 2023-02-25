
import modin.pandas as pd

from yahoo_fin import stock_info
from Control.Util_Controllers.modin_utils import on_demand_garbage_collect

def stock_parser_worker(ticker, curr_idx, df_index_ptr, start_date=None, end_date=None):
    """
    Extracts stock data for a given ticker and time range.

    Arguments:
        ticker (tuple): Tuple containing the ticker symbol, name, and exchange.
        curr_idx (int): Current index in the list of tickers being parsed.
        df_index_ptr (int): Starting index for the data frame being created.
        start_date (str, optional): Start date for the data to be retrieved. Defaults to None.
        end_date (str, optional): End date for the data to be retrieved. Defaults to None.

    Returns:
        tuple: Tuple containing a list of dictionaries with the stock data, 
        the current index in the list of tickers, and the ending index for the data frame.
    """
    # Create an empty data frame with the necessary columns
    base_data_frame = pd.DataFrame(columns=['tickerId', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume'])
    
    # Set error flag to false
    e_flag = False
    
    try:
        # Retrieve stock data from Yahoo Finance API for the given ticker and time range
        current_data_frame = stock_info.get_data(ticker[2], index_as_date=False, start_date=start_date, end_date=end_date)
    except Exception as e:
        # Set error flag to true if an exception occurs
        e_flag = True
    
    # If no error occurred, add the tickerId column and concatenate the data frames
    if not e_flag:
        current_data_frame['tickerId'] = ticker[0]
        current_data_frame.drop('ticker', axis=1, inplace=True)
        base_data_frame = pd.concat([base_data_frame, current_data_frame], axis=0)

    # Remove any rows with missing data and reset the index
    base_data_frame.dropna(inplace=True)
    base_data_frame.index = range(df_index_ptr, df_index_ptr + base_data_frame.shape[0])
    base_data_frame.index.rename('stockId', inplace=True)

    # Convert the data frame to a list of dictionaries and perform garbage collection
    base_list = base_data_frame.to_dict('records')
    on_demand_garbage_collect()
    
    # Return the list of dictionaries, the current index, and the ending index
    return base_list, curr_idx + 1, df_index_ptr + base_data_frame.shape[0]

def stock_parser(ticker, start_date=None, end_date=None):
    '''
    Function that parses all the stock values of a `ticker` into a `list` of `dictionaries`.

    Arguments:
        `ticker`: Data for the current ticker retrieved from the `DataBase`.
    '''
    curr_idx, df_index_ptr = 0, 0
    base_list, curr_idx, df_index_ptr = stock_parser_worker(ticker, curr_idx, df_index_ptr, start_date=start_date, end_date=end_date)
    # check if base_list is empty
    if base_list:
        return base_list
