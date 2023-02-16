from sqlalchemy import select

def base_conditional_in_selector(table, columnName, columnValues):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `table`: User must provide the Table of the `DataBase` from which the data will be extracted from.
        `columnName`: User must provide the `Name` of the `Column` that needs to be updated.
        `columnValue`: User must provide the `Value` of the `Column` `Where` the `Update` must happen.

    SQL query example:
        SELECT * FROM `table`
        WHERE `table`.`columnName` IN (`columnValues`)
    '''
    try:
        return select(table).where(columnName.in_(columnValues))
    except:
        pass
        # print('Something went wrong with selection.') # TODO: This must be a logger.
