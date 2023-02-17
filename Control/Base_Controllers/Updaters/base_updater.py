from sqlalchemy import update

def base_updater(table, values):
    '''
    Function that executes the base `SQL` UPDATE `query`.

    Arguments:
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `values`: User must provide a `list` of `dictionaries` with the values that need to be updated to the `table` of the `DataBase`.

    SQL query example:
        UPDATE `table` SET `values`
    '''
    try:
        (update(table), values)
    except:
        pass
        # print('Something went wrong with update.') # TODO: This must be a logger.
