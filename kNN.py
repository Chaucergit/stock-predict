# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import os
import numpy as np
import operator
from stock import Stock


class kNN(Stock):
    def __init__(self):
        Stock.__init__(self)
        self.reload_all()

    def __del__(self):
        pass

    def __classify0(self, data_for_classify, training_data, training_label, k):
        pass

    def predict(self):
        for code in self.data:
            print code
            volume, chg_p, vma5 = Stock.get_col().index("volume"), Stock.get_col().index("chg_p"), Stock.get_col().index("vma5")
            data_array = np.array(self.data[code])
            try:
                chg_p_array, vma5_array, volume_array = np.float32(data_array[:,chg_p]), np.float32(data_array[:,vma5]), np.float32(data_array[:,volume])
                training_data = volume_array
                training_label = [["down", "up"][int(x > 0.0)] for x in chg_p_array]
                print training_label
            except:
                print data_array


if __name__ == '__main__':
    k = kNN()
    k.predict()
