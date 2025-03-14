import logging
from sqlalchemy import select, desc

def base_conditional_ordered_limited_selector(table, columnName, columnValue, orderColumn, limitNumber=None, descending=False):
    '''
    Function that executes the base SQL SELECT query.

    Arguments:
        table: User must provide the Table of the DataBase from which the data will be extracted from.
        columnName: User must provide the Name of the Column that needs to be updated.
        columnValue: User must provide the Value of the Column Where the Update must happen.
        orderColumn: User must provide the Name of the Column on which the Order By must happen.
        limitNumber: User can provide the Number of the Limit of the results. If None, there is no limit.
        descending: If set to True, orders the results in descending order. Default is False.

    SQL query example:
        SELECT * FROM table
        WHERE table.columnName = columnValue
        ORDER BY orderColumn [DESC]
        [LIMIT limitNumber]
    '''
    try:
        query = select(table).where(columnName == columnValue)
        if descending:
            query = query.order_by(desc(orderColumn))
        else:
            query = query.order_by(orderColumn)
        
        if limitNumber is not None:
            query = query.limit(limitNumber)

        return query
    except Exception as e:
        logger = logging.getLogger('Logger')
        logger.error(f'Something went wrong with conditional ordered limited selection: {e}')
