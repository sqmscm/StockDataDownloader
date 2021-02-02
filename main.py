import pymssql
import os
from config import log

if __name__ == '__main__':
    # server    数据库服务器名称或IP
    # user      用户名
    # password  密码
    # database  数据库名称
    server = 'stock8903.database.windows.net'
    database = 'stock'
    user = 'qiming'
    password = '12345678@Gatech'
    log.info(f'Trying to connect {server}')
    try:
        conn = pymssql.connect(server, user, password, database)  # using username + password
        conn.close()
    except Exception as e:
        log.error(e)
        log.info('Connection Failed')
