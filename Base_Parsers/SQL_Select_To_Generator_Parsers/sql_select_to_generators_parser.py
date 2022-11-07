def sql_select_to_generator(tickers):
    for row in tickers:
        yield row

def sql_select_to_list(tickers):
    return [row for row in tickers]
