from sqlalchemy import select
from sqlalchemy import func

def base_count_selector(table):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.

    SQL query example:
        SELECT COUNT(*) FROM `table`
    '''
    try:
        return select(func.count()).select_from(table)
    except:
        pass
        # print('Something went wrong with selection.') # TODO: This must be a logger.
