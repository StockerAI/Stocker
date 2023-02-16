def silent_executioner(connection, SIUD):
    '''
    Function that silently executes the base `SQL query`.

    Arguments:
        `connection`: User must provide the Connection of the `DataBase`.
        `SIUD`: Stands for `Select`, `Insert`, `Update` and `Delete` queries.
    '''
    try:
        return connection.execution_options(stream_results=False).execute(SIUD)
    except:
        pass
        # print('Something went wrong with execution.') # TODO: This must be a logger.