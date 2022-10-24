from sqlalchemy import insert

def base_inserter(connection, table, values):
    try:
        connection.execute(insert(table), values)
    except:
        print('Something went wrong with insertion.')