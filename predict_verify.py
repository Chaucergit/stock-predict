# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import os
import numpy as np
import operator
import time
import logging
from stock import Stock
from error import trace_log
from collections import defaultdict
from mydir import mydir
from dataProcess import norm, classify0


class PredictVerify(Stock):
    up_code = None

    def __init__(self, close_data_file, predict_file):
        Stock.__init__(self)
        self.reload_all(close_data_file)
        with open(os.path.join(mydir(), "data", predict_file), "r") as f:
            code_list = f.read().split('\n')
            self.up_code = code_list

    def __del__(self):
        pass

    def verify(self):
        up5 = 0
        up1 = 0
        up9 = 0
        up = []
        chg_p = Stock.get_col().index("chg_p")
        for code in self.up_code:
            data_array = np.array(self.data[code])
            try:
                chg_p_array = np.float32(data_array[:,chg_p])
                if chg_p_array[-1] >= 1.0:
                    up1 += 1
                    up.append((code, chg_p_array[-1]))
                if chg_p_array[-1] >= 5.0:
                    up5 += 1
                if chg_p_array[-1] >= 9.0:
                    up9 += 1
            except:
                logging.error("%s failed" % code)
                trace_log()
        print "up5 = %.2f, up1 = %.2f, up9 = %.2f" % (float(up5)/float(len(self.up_code)), float(up1)/float(len(self.up_code)), float(up9)/float(len(self.up_code)))
        print up


if __name__ == '__main__':
    import sys
    k = PredictVerify(sys.argv[1], sys.argv[2])
    k.verify()
