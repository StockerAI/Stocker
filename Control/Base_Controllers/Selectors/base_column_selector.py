from sqlalchemy import select

def base_column_selector(columnName, table):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `column`: User must provide the Column name of the `DataBase` from which the data will be extracted from, 
        `table`: User must provide the Table of the `DataBase` from which the data will be extracted from.

    SQL query example:
        SELECT `column1` FROM `table`
    '''
    try:
        return select(columnName).select_from(table)
    except:
        pass
        # print('Something went wrong with selection.') # TODO: This must be a logger.
