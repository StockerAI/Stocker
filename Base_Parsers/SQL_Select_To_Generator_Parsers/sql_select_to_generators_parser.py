def sql_select_to_generator(tickers):
    for row in tickers:
        yield row
