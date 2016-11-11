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


class kNN(Stock):
    def __init__(self):
        Stock.__init__(self)
        self.reload_all()

    def __del__(self):
        pass

    def __classify0(self, data_for_classify, training_data, training_label, k):
        training_data_size = training_data.shape[0]
        diffMat = np.tile(data_for_classify, training_data_size) - training_data
        #sqDiffMat = diffMat**2
        #sqDistances = sqDiffMat.sum(axis=1)
        #distances = sqDistances**0.5
        sortedDistIndicies = diffMat.argsort()
        classCount={}
        for i in range(k):
            voteIlabel = training_label[sortedDistIndicies[i]]
            classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]

    def predict(self):
        result = defaultdict(set)
        for code in self.data:
            volume, chg_p, vma5 = Stock.get_col().index("volume"), Stock.get_col().index("chg_p"), Stock.get_col().index("vma5")
            data_array = np.array(self.data[code])
            try:
                chg_p_array, vma5_array, volume_array = np.float32(data_array[:,chg_p]), np.float32(data_array[:,vma5]), np.float32(data_array[:,volume])
                training_data = volume_array
                training_label = [["down", "up"][int(x > 5.0)] for x in chg_p_array]
                trend = self.__classify0(vma5_array[-1], training_data, training_label, 5)
                result[trend].add(code)
            except:
                trace_log()
                pass
        return result


if __name__ == '__main__':
    k = kNN()
    r = k.predict()
    with open(os.path.join(mydir(), "data", time.strftime("%Y%m%d", time.localtime())+".txt"), "w") as f:
        for key in r:
            f.write("#######" + key + "######\n")
            for code in r[key]:
                f.write(code + "\n")
