import pyodbc
from time import sleep
from config import log, conn_str
from utils import download_latest

if __name__ == '__main__':
    log.info('Trying to connect...')
    conn_trails = 0
    conn = None
    while conn_trails < 5:
        try:
            conn = pyodbc.connect(conn_str)
            break
        except Exception as e:
            log.error(e)
            conn_trails += 1
            log.info(f'Connection Failed {conn_trails}.')
            sleep(30)
    else:
        log.error('Could not connect to database.')
        exit()

    download_latest(conn, log)
    conn.close()

