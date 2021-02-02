import pyodbc
import os
from config import log, conn_str
from utils import download_latest

if __name__ == '__main__':
    log.info('Trying to connect...')
    try:
        conn = pyodbc.connect(conn_str)  # using username + password
        download_latest(conn, log)
        conn.close()
    except Exception as e:
        log.error(e)
        log.info('Connection Failed')
