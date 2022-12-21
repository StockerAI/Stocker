from sqlalchemy import insert

def base_inserter(connection, table, values):
    '''
    Function that executes the base `SQL` INSERT `query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `values`: User must provide a `list` of `dictionaries` with the values that need to be added to the `table` of the `DataBase`.

    SQL query example:
        INSERT INTO `table` VALUES `values`
    '''
    try:
        connection.execution_options(stream_results=False).execute(insert(table), values)
    except:
        print('Something went wrong with insertion.') # TODO: This must be a logger.
