def sql_select_to_generator(tickers):
    '''
    Function that returns a `generator` of tickers.

    Arguments:
        `tickers`: The Tickers from the `DataBase`.
    '''
    for row in tickers:
        yield row

def sql_select_to_list(tickers):
    '''
    Function that returns a `list` of tickers.

    Arguments:
        `tickers`: The Tickers from the `DataBase`.
    '''
    return [row for row in tickers]
