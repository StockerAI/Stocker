import logging
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
    except Exception as e:
        logger = logging.getLogger('Logger')
        logger.error(f'Something went wrong with count selection: {e}')