import logging
from sqlalchemy import select

def base_distinct_column_selector(columnName, table):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `column`: User must provide the Column name of the `DataBase` from which the data will be extracted from, 
        `table`: User must provide the Table of the `DataBase` from which the data will be extracted from.

    SQL query example:
        SELECT DISTINCT `column1` FROM `table`
    '''
    try:
        return select(columnName).select_from(table).distinct()
    except Exception as e:
        logger = logging.getLogger('Logger')
        logger.error(f'Something went wrong with distinct selection: {e}')