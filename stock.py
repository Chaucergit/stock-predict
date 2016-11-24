# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import os
import json
import re
import logging
import time
import cPickle
import threading
import cProfile
from collections import defaultdict
from httpRequest import HttpRequest
from error import trace_log
from bs4 import BeautifulSoup
from mydir import mydir


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
    code = defaultdict(set)
    data = defaultdict(set)

    def __init__(self):
        self.code.clear()
        bs = BeautifulSoup(HttpRequest("http://quote.eastmoney.com/stocklist.html").get(), "lxml")
        for a in bs.find('div', id='quotesearch').find_all('a'):
            try:
                rg = re.match(".*(sh|sz)([0-9]{6})\.html", a['href']).groups()
                self.code[rg[0]].add(rg[1])
            except:
                pass
        for key in self.code:
            logging.info("%s: %d" % (key, len(self.code[key])))

    def __del__(self):
        pass

    def refresh_all(self):
        self.data.clear()
        for key in self.code:
            for code in self.code[key]:
                def retrieve_data(key, code):
                    try:
                        logging.info("get daily data of %s" % (key+code))
                        s = re.compile(r",(\d+)").sub(r"\1", HttpRequest(DAILY_PRICE_URL % (key+code)).get())
                        s = re.compile(r"(\d+)\_(\d+)\_(\d+)").sub(r"\1\2\3", s)
                        self.data[code] = json.loads(s)["record"]
                    except:
                        pass
                retrieve_data(key, code)
        return self.data

    def fast_refresh_all(self):
        self.data.clear()
        for key in self.code:
            all_codes = list(self.code[key])
            for start in range(0, len(self.code[key]), 10):
                codes = all_codes[start:start+10]

                def retrieve_data(key, codes):
                    threads = []
                    for code in codes:
                        def __retrieve_data(key, code):
                            try:
                                logging.info("get daily data of %s" % (key+code))
                                s = re.compile(r",(\d+)").sub(r"\1", HttpRequest(DAILY_PRICE_URL % (key+code)).get())
                                s = re.compile(r"(\d+)\_(\d+)\_(\d+)").sub(r"\1\2\3", s)
                                self.data[code] = json.loads(s)["record"]
                            except:
                                pass
                        t = threading.Thread(target=__retrieve_data, args=(key, code))
                        t.setDaemon(True)
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                retrieve_data(key, codes)
        return self.data

    def save_all(self):
        filename = os.path.join(mydir(), "data", time.strftime("%Y%m%d", time.localtime())+".pkl")
        try:
            logging.info("dump all the data to file %s" % filename)
            with open(filename, "w") as f:
                cPickle.dump(self.data, f)
                return os.path.basename(filename)
        except:
            trace_log()
            return None

    def reload_all(self, name=time.strftime("%Y%m%d", time.localtime())+".pkl"):
        filename = os.path.join(mydir(), "data", name)
        if not os.path.exists(filename):
            self.fast_refresh_all()
            self.save_all()
        else:
            try:
                logging.info("load all the data from file %s" % filename)
                with open(filename, "r") as f:
                    self.data = cPickle.load(f)
            except:
                trace_log()
                self.fast_refresh_all()
                self.save_all()
        return self.data

    @staticmethod
    def get_col():
        return DAILY_PRICE_COL

    @staticmethod
    def get_col_cn():
        return DAILY_PRICE_COL_CN


if __name__ == '__main__':
    # unittest
    import unittest

    class MyTest(unittest.TestCase):
        def test_get_daily(self):
            s = Stock()
            self.assertIsNotNone(s.refresh_all())
            self.assertIsNotNone(s.fast_refresh_all())
            self.assertIsNotNone(s.save_all())
            self.assertNotEqual(s.reload_all(), {})

        def test_get_col(self):
            self.assertEqual(Stock.get_col(), DAILY_PRICE_COL)
            self.assertEqual(Stock.get_col_cn(), DAILY_PRICE_COL_CN)
    unittest.main()

    # performance testing
    s = Stock()
    cProfile.run("s.refresh_all()")
    cProfile.run("s.fast_refresh_all()")
