import pyodbc
import os
from config import log

if __name__ == '__main__':
    log.info('Trying to connect...')
    try:
        conn = pyodbc.connect(os.environ['CONNECTION_STRING'])  # using username + password
        conn.close()
    except Exception as e:
        log.error(e)
        log.info('Connection Failed')
