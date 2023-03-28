import logging
from sqlalchemy import select

def base_selector(table):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `table`: User must provide the Table of the `DataBase` from which the data will be extracted from.

    SQL query example:
        SELECT * FROM `table`
    '''
    try:
        return select(table)
    except:
        logger = logging.getLogger('Logger')
        logger.error('Something went wrong with selection.')