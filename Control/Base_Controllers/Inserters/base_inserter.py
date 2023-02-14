from sqlalchemy import insert

def base_inserter(table, values):
    '''
    Function that executes the base `SQL` INSERT `query`.

    Arguments:
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `values`: User must provide a `list` of `dictionaries` with the values that need to be added to the `table` of the `DataBase`.

    SQL query example:
        INSERT INTO `table` VALUES `values`
    '''
    try:
        (insert(table), values)
    except:
        pass
        # print('Something went wrong with insertion.') # TODO: This must be a logger.
