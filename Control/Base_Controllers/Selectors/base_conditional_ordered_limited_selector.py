import logging 
from sqlalchemy import select

def base_conditional_ordered_limited_selector(table, columnName, columnValue, orderColumn, limitNumber):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `columnName`: User must provide the `Name` of the `Column` that needs to be updated.
        `columnValue`: User must provide the `Value` of the `Column` `Where` the `Update` must happen.
        `orderColumn`: User must provide the `Name` of the `Column` on which the `Order By` must happen.
        `limitNumber`: User must proveide the `Number` of the `Limit` of the results if negative, there is no limit.

    SQL query example:
        SELECT * FROM `table`
        WHERE `table`.`columnName` = `columnValue`
        ORDER BY `orderColumn`
        LIMIT = `limitNumber`
    '''
    try:
        if limitNumber >= 0:
            return select(table).where(columnName == columnValue).order_by(orderColumn).limit(limitNumber)
        else:
            return select(table).where(columnName == columnValue).order_by(orderColumn)
    except:
        logger = logging.getLogger('Logger')
        logger.error('Something went wrong with conditional ordered limited selection.')