from sqlalchemy import update

def base_conditional_updater(connection, table, columnName, columnValue, values):
    '''
    Function that executes the base `SQL` UPDATE `query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `values`: User must provide a `list` of `dictionaries` with the values that need to be added to the `table` of the `DataBase`.

    SQL query example:
        INSERT INTO `table` VALUES `values`
    '''
    try:
        connection.execute(update(table).where(columnName == columnValue), values)
    except:
        print('Something went wrong with conditional update.')
