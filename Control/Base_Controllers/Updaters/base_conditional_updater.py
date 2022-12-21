from sqlalchemy import update

def base_conditional_updater(connection, table, columnName, columnValue, values):
    '''
    Function that executes the base `SQL` UPDATE `query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `columnName`: User must provide the `Name` of the `Column` that needs to be updated.
        `columnValue`: User must provide the `Value` of the `Column` `Where` the `Update` must happen.
        `values`: User must provide a `list` of `dictionaries` with the values that need to be updated to the `table` of the `DataBase`.

    SQL query example:
        UPDATE `table` SET `values` WHERE `condition`
    '''
    try:
        connection.execution_options(stream_results=False).execute(update(table).where(columnName == columnValue), values)
    except:
        print('Something went wrong with conditional update.') # TODO: This must be a logger.
