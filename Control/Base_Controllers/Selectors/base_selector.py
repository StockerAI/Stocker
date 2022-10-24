from sqlalchemy import select

def base_selector(connection, table):
    try:
        return connection.execute(select(table))
    except:
        print('Something went wrong with selection.')