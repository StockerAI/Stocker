from Model.config import config
import psycopg2

class Engine_Creator():
    def __init__(self) -> None:
        pass
    def __enter__(self):
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)

            # create a cursor
            cur = self.conn.cursor()
            
            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)
        
            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')