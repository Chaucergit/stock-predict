# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import os
import numpy as np
import operator
import time
from stock import Stock
from error import trace_log
from mydir import mydir


class gold(Stock):
    def __init__(self):
        Stock.__init__(self)
        self.reload_all()

    def __del__(self):
        pass

    def predict(self):
        result = {}
        for code in self.data:
            date, close, chg_p = Stock.get_col().index("date"), Stock.get_col().index("close"), Stock.get_col().index("chg_p")
            try:
                last_date = self.data[code][-1][0]
                if last_date != time.strftime("%Y-%m-%d", time.localtime()):
                    continue
            except:
                continue
            data_array = np.array(self.data[code])
            try:
                close_array, chg_p_array = np.float32(data_array[:,close]), np.float32(data_array[:,chg_p])
                def gold_predict(close_array):
                    close_array = close_array[-10:]
                    max_close = max(close_array)
                    min_close = min(close_array)
                    if close_array[-1] < max_close and max_close == close_array[-2]:
                        if (max_close - min_close)/min_close > 0.1 :
                            ratio = (max_close - close_array[-1]) / (max_close - min_close)
                            if ratio < (0.382+0.010) and ratio > (0.382-0.010):
                                result[code] = 2*max_close-close_array[-1]
                                return True
                    return False
                top_5_close_array = close_array[-5:]
                if not gold_predict(top_5_close_array):
                    top_10_close_array = close_array[-10:]
                    gold_predict(top_10_close_array)
            except:
                trace_log()
                pass
        return result.items()


if __name__ == '__main__':
    k = gold()
    r = k.predict()
    with open(os.path.join(mydir(), "data", time.strftime("gold_%Y%m%d", time.localtime())+".txt"), "w") as f:
        for code, price in r[0:10]:
            f.write("%s %.2f\n"%(code, price))
