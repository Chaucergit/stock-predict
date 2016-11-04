# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import json
import re
import logging
import time
from httpRequest import HttpRequest
from error import trace_log
from bs4 import BeautifulSoup


DAILY_PRICE_URL = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last'
DAILY_PRICE_COL = (
    'date',
    'open',
    'high',
    'close',
    'low',
    'volume',
    'chg',
    'chg_p',
    'ma5',
    'ma10',
    'ma20',
    'vma5',
    'vma10',
    'vma20',
    'turnover'
)
DAILY_PRICE_COL_CN = (
    '日期',
    '开盘价',
    '最高价',
    '收盘价',
    '最低价',
    '成交量',
    '涨跌额',
    '涨跌幅',
    '5日均价',
    '10日均价',
    '20日均价',
    '5日均量',
    '10日均量',
    '20日均量',
    '换手率'
)


class Stock:
    code = {}
    data = {}

    def __init__(self):
        self.code = {}
        bs = BeautifulSoup(HttpRequest("http://quote.eastmoney.com/stocklist.html").get(), "lxml")
        for a in bs.find('div', id='quotesearch').find_all('a'):
            try:
                rg = re.match(".*(sh|sz)([0-9]{6})\.html", a['href']).groups()
                if rg[0] not in self.code:
                    self.code[rg[0]] = []
                self.code[rg[0]].append(rg[1])
            except:
                trace_log()
        for key in self.code:
            logging.error("%s: %d" % (key, len(self.code[key])))
        pass

    def __del__(self):
        print self.code
        print self.data
        pass

    def get_single(self, code):
        for key in self.code:
            if code in self.code[key]:
                logging.error("get daily data of %s" % (key+code))
                try:
                    return json.loads(HttpRequest(DAILY_PRICE_URL % (key+code)).get())["record"]
                except:
                    trace_log()
                    break
        return None

    def get_all(self):
        self.data = {}
        for key in self.code:
            for code in self.code[key]:
                for i in range(0, 5):
                    try:
                        logging.error("get daily data of %s" % (key+code))
                        self.data[code] = json.loads(HttpRequest(DAILY_PRICE_URL % (key+code)).get())["record"]
                        break
                    except:
                        trace_log()
                        time.sleep(5)
        return self.data

    @staticmethod
    def get_col():
        return DAILY_PRICE_COL

    @staticmethod
    def get_col_cn():
        return DAILY_PRICE_COL_CN


if __name__ == '__main__':
    import unittest

    class MyTest(unittest.TestCase):
        def test_get_daily(self):
            self.assertIsNotNone(Stock().get_single("601633"))
            self.assertIsNone(Stock().get_single("xxxxxx"))
            self.assertIsNotNone(Stock().get_all())

        def test_get_col(self):
            self.assertEqual(Stock.get_col(), DAILY_PRICE_COL)
            self.assertEqual(Stock.get_col_cn(), DAILY_PRICE_COL_CN)

    unittest.main()
