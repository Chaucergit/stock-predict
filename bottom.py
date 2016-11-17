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
from collections import defaultdict
from mydir import mydir
from dataProcess import classify0


class bottom(Stock):
    def __init__(self):
        Stock.__init__(self)
        self.reload_all()

    def __del__(self):
        pass

    def predict(self):
        result = {}
        for code in self.data:
            volume, chg_p, vma5, ma5, close = Stock.get_col().index("volume"), Stock.get_col().index("chg_p"), Stock.get_col().index("vma5"), Stock.get_col().index("ma5"), Stock.get_col().index("close")
            data_array = np.array(self.data[code])
            try:
                chg_p_array, vma5_array, volume_array, ma5_array, close_array = np.float32(data_array[:,chg_p]), np.float32(data_array[:,vma5]), np.float32(data_array[:,volume]), np.float32(data_array[:,ma5]), np.float32(data_array[:,close])
                if close_array[-1] < ma5_array[-1] and volume_array[-1] < vma5_array[-1]:
                    down_number = 0
                    for c in chg_p_array[-5:]:
                        if c < 0.0:
                            down_number += 1
                    result[code] = down_number
            except:
                trace_log()
                pass
        sorted_result = sorted(result.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_result


if __name__ == '__main__':
    k = bottom()
    r = k.predict()
    with open(os.path.join(mydir(), "data", time.strftime("bottom_%Y%m%d", time.localtime())+".txt"), "w") as f:
        for code, down_number in r:
            f.write(code + "\n")
