from sqlalchemy import select

def base_selector(connection, table):
    '''
    Function that executes the base `SQL` SELECT `query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `table`: User must provide the Table od the `DataBase` from which the data will be extracted from.

    SQL query example:
        SELECT * FROM `table`
    '''
    try:
        return connection.execute(select(table))
    except:
        print('Something went wrong with selection.')