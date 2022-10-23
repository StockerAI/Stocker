from sqlalchemy import insert

def base_inserter(connection, table, values):
    connection.execute(insert(table), values)
