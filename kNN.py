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
from dataProcess import norm, classify0


class kNN(Stock):
    def __init__(self):
        Stock.__init__(self)
        self.reload_all()

    def __del__(self):
        pass

    def predict(self):
        result = []
        for code in self.data:
            volume, chg_p, vma5 = Stock.get_col().index("volume"), Stock.get_col().index("chg_p"), Stock.get_col().index("vma5")
            data_array = np.array(self.data[code])
            try:
                chg_p_array, vma5_array, volume_array = np.float32(data_array[:,chg_p]), np.float32(data_array[:,vma5]), np.float32(data_array[:,volume])
                training_data = []
                for v in volume_array:
                    training_data.append([v])
                training_label = [["down", "up"][int(x > 5.0)] for x in chg_p_array]
                trend, percent = classify0([vma5_array[-1]], np.array(training_data), training_label, 5)
                if trend == "up":
                    result.append((code, percent))
            except:
                trace_log()
                pass
        sorted_result = sorted(result, key=operator.itemgetter(1), reverse=True)
        return sorted_result


if __name__ == '__main__':
    k = kNN()
    r = k.predict()
    with open(os.path.join(mydir(), "data", time.strftime("kNN_%Y%m%d", time.localtime())+".txt"), "w") as f:
        for code, percent in r:
            f.write(code + "\n")
