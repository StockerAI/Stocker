from sqlalchemy import select, desc

def base_conditional_ordered_limited_selector(connection, table, columnName, columnValue, orderColumn, limitNumber):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.
        `columnName`: User must provide the `Name` of the `Column` that needs to be updated.
        `columnValue`: User must provide the `Value` of the `Column` `Where` the `Update` must happen.
        `orderColumn`: User must provide the `Name` of the `Column` on which the `Order By` must happen.
        `limitNumber`: User must proveide the `Number` of the `Limit` of the results.

    SQL query example:
        SELECT * FROM `table`
        WHERE `table`.`columnName` = `columnValue`
        ORDER BY `orderColumn`
        LIMIT = 1
    '''
    try:
        return connection.execution_options(stream_results=False).execute(select(table).where(columnName == columnValue).order_by(desc(orderColumn)).limit(limitNumber))
    except:
        print('Something went wrong with conditional ordered limited selection.') # TODO: This must be a logger.
