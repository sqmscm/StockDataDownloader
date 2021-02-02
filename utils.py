import requests
import csv
import time
import datetime
import random


def download_all(conn, logger):
    """
    Download all stock data in 2 years.

    :param conn: sql connection instance
    :param logger: logger instance
    :return: None
    """
    # setup slices, 24 in total
    slices = [f'year{x}month{y}' for x in [2, 1] for y in range(12, 0, -1)]
    for slice in slices:
        download_intraday_extended(conn, logger, slice)


def download_latest(conn, logger):
    """
    Download the latest stock data. Should be run routinely.

    :param conn: sql connection instance
    :param logger: logger instance
    :return: None
    """
    download_intraday_extended(conn, logger)


def download_intraday_extended(conn, logger, slice='year1month1'):
    """
    Download the stock data using extended intraday API.

    :param conn: sql connection instance
    :param logger: logger instance
    :param slice: Each slice is a 30-day window, with 'year1month1' being the most recent and 'year2month12' being the farthest from today. By default, slice=year1month1
    :return: None
    """
    # 下载地址
    url_pattern = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={}&interval=5min&slice={}&adjusted=true&apikey=8X20WDQGP22OU1PN"
    Symbol = 'UVXY'
    path_root = 'stocks/data/'
    logger.info(f'Start downloading slice {slice}')
    # 判断curStocks表是否为空，否,则遍历curStocks，是,则将Stocks表中的所有股票代码插入curStocks表，遍历Stocks
    # 判断curStocks表是否为空
    cursor0 = conn.cursor()
    cursor0.execute('select count(*) from curStocks')
    result0 = cursor0.fetchall()
    count = int(result0[0][0])
    cursor0.close()
    if count == 0:
        # 遍历Stocks表
        cursor1 = conn.cursor()
        cursor1.execute('select count(*) from Stocks')
        result1 = cursor1.fetchall()
        count = int(result1[0][0])
        cursor1.execute('insert into curStocks (Symbol) select Symbol from Stocks')
        cursor1.close()
        conn.commit()

    while count > 0:
        # 遍历curStocks表
        cursor1 = conn.cursor()
        cursor1.execute('SELECT Symbol FROM curStocks')
        result = cursor1.fetchall()
        cursor1.close()

        for line in result:
            Symbol = line[0].strip()
            logger.info(f'Current stock code: {Symbol}')

            # 下载地址url
            url = url_pattern.format(Symbol, slice)
            logger.debug(url)

            try:
                # 把下载地址发送给requests模块
                f = requests.get(url, timeout=10)  # 设置超时

                # 下载文件
                path = f'{path_root}{Symbol}_{slice}.csv'
                logger.debug(f'File saved to: {path}')
                with open(path, "wb") as code:
                    code.write(f.content)

            except Exception as e:
                logger.debug(e)
                logger.error(Symbol + '下载失败')
                # time.sleep(random.randint(30, 60))
                continue
            # logger.debug(curDate)
            # 取出上次的数据日期
            cursor0 = conn.cursor()
            cursor0.execute('select max(timestamp) from IntradayQuotes where Symbol = ?;', Symbol)
            result0 = cursor0.fetchall()
            cursor0.close()
            oldDate = result0[0][0] if result0[0][0] else None
            logger.info(f'Last record in database: {oldDate}')
            # 写入数据库
            with open(path, 'r') as csvfile:
                next(csvfile)
                cursor2 = conn.cursor()
                read = csv.reader(csvfile)  # 逐行读取csv文件，并写入
                for i, one_line in enumerate(read):
                    newDate = datetime.datetime.strptime(one_line[0], '%Y-%m-%d %H:%M:%S')
                    if oldDate and newDate <= oldDate:
                        logger.info(f'Imported {i} new records.')
                        break
                    cursor2.execute("INSERT INTO IntradayQuotes VALUES (?,?,?,?,?,?,?)", (
                        Symbol, one_line[0], one_line[1], one_line[2], one_line[3], one_line[4], one_line[5]))
                else:
                    logger.info(f'Imported {i + 1} new records.')
                cursor2.close()

            # 更新curStocks表
            cursor3 = conn.cursor()
            cursor3.execute("delete from curStocks where Symbol = ?", Symbol)
            cursor3.close()

            conn.commit()
            wait_time = random.randint(10, 30)
            logger.debug(f'Waiting for {wait_time} seconds to continue...')
            time.sleep(wait_time)

        # 检查curStocks是否还有未下载的股票
        cursor4 = conn.cursor()
        cursor4.execute('select count(*) from curStocks')
        result4 = cursor4.fetchall()
        count = int(result4[0][0])
        cursor4.close()
        if count > 0:
            logger.info('本轮下载失败数量：' + str(count))

    logger.info(f'Slice {slice} has been downloaded.')
