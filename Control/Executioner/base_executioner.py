def base_executioner(connection, SIUD):
    '''
    Function that executes the base `SQL query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `SIUD`: Stands for `Select`, `Insert`, `Update` and `Delete` queries.
    '''
    return connection.execute(SIUD)