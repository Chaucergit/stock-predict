# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import os
import numpy as np
import operator
from collections import defaultdict


#
# new value = (old value - min)/(max - min)
#
def norm(data_set):
    mins = data_set.min(0)
    maxs = data_set.max(0)
    ranges = maxs - mins
    m = data_set.shape[0]
    return (data_set - np.tile(mins, (m,1))) / np.tile(ranges, (m,1)), ranges, mins


#
# kNN
#
def classify0(data_in, training_data, training_label, k):
    training_data_size = training_data.shape[0]
    diff_mat = np.tile(data_in, (training_data_size, 1)) - training_data
    sq_diff_mat = diff_mat**2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances**0.5
    sorted_distances = distances.argsort()
    class_count = {}
    for i in range(k):
        vote_label = training_label[sorted_distances[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


if __name__ == '__main__':
    training_data = np.array([[1, 2, 3], [3, 2, 4], [5, 2, 0]])
    training_label = ["up", "down", "down"]
    data_in = [4, 4, 4]
    print classify0(data_in, training_data, training_label, 3)

    training_data = np.array([[1], [4], [0]])
    training_label = ["up", "down", "down"]
    data_in = [4]
