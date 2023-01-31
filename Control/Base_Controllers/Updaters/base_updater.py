from sqlalchemy import update

def base_updater(connection, table, values):
    '''
    Function that executes the base `SQL` UPDATE `query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `values`: User must provide a `list` of `dictionaries` with the values that need to be updated to the `table` of the `DataBase`.

    SQL query example:
        UPDATE `table` SET `values`
    '''
    try:
        connection.execution_options(stream_results=False).execute(update(table), values)
    except:
        pass
        # print('Something went wrong with update.') # TODO: This must be a logger.
