from sqlalchemy import select

def base_selector(table):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.

    SQL query example:
        SELECT * FROM `table`
    '''
    try:
        return select(table)
    except:
        pass
        # print('Something went wrong with selection.') # TODO: This must be a logger.
