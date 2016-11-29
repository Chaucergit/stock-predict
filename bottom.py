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


class bottom(Stock):
    def __init__(self):
        Stock.__init__(self)
        self.reload_all()

    def __del__(self):
        pass

    def predict(self):
        result = {}
        for code in self.data:
            volume, chg_p, vma5, ma5, close, high = Stock.get_col().index("volume"), Stock.get_col().index("chg_p"), Stock.get_col().index("vma5"), Stock.get_col().index("ma5"), Stock.get_col().index("close"), Stock.get_col().index("high")
            try:
                last_date = self.data[code][-1][0]
                if last_date != time.strftime("%Y-%m-%d", time.localtime()):
                    continue
            except:
                continue
            data_array = np.array(self.data[code])
            try:
                chg_p_array, vma5_array, volume_array, ma5_array, close_array, high_array = np.float32(data_array[:,chg_p]), np.float32(data_array[:,vma5]), np.float32(data_array[:,volume]), np.float32(data_array[:,ma5]), np.float32(data_array[:,close]), np.float32(data_array[:,high])
                # 判断跳空
                jumped = False
                for i in range(-1, -10, -1):
                    if high_array[i] < close_array[i-1]:
                        jumped = True
                        break
                if jumped and chg_p_array[-1] > 3.0:
                    down_number = 0
                    for c in chg_p_array[-10:]:
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
        for code, down_number in r[0:10]:
            f.write(code + "\n")
