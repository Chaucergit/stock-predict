# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import numpy as np
import operator
from math import log


#
# new value = (old value - min)/(max - min)
#
def norm(data_in):
    mins = data_in.min(0)
    maxs = data_in.max(0)
    ranges = maxs - mins
    m = data_in.shape[0]
    return (data_in - np.tile(mins, (m,1))) / np.tile(ranges, (m,1)), ranges, mins


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
    return sorted_class_count[0][0], float(sorted_class_count[0][1])/float(k)


#
# calculate shannon entropy
# input data_in should be like
# [ [1,1,'yes'],
#   [1,0,'no' ],
#   [0,1,'no' ],
#   [0,1,'no' ] ]
#
def calc_shannon_entropy(data_in):
    num_entries = len(data_in)
    class_summary = {}
    for a in data_in:
        c = a[-1]
        if c not in class_summary:
            class_summary[c] = 1
        else:
            class_summary[c] += 1
    shannon_entropy = 0.0
    for k in class_summary:
        prob = float(class_summary[k])/float(num_entries)
        shannon_entropy += -prob * log(prob,2)
    return shannon_entropy


#
# split data set according to axis and value
# input data_in should be like
# [ [1,1,'yes'],
#   [1,0,'no' ],
#   [0,1,'no' ],
#   [0,1,'no' ] ]
#
def split_data_set(data_in, axis, value):
    ret_data_set = []
    for a in data_in:
        if a[axis] == value:
            temp = a[:axis]
            temp.extend(a[axis+1:])
            ret_data_set.append(temp)
    return ret_data_set


#
# choose the best feature id for best shannon entropy
# input data_in should be like
# [ [1,1,'yes'],
#   [1,0,'no' ],
#   [0,1,'no' ],
#   [0,1,'no' ] ]
#
def choose_best_feature_for_best_shannon_entropy(data_in):
    num_features = len(data_in[0])-1
    base_entropy = calc_shannon_entropy(data_in)
    best_info_gain, best_feature = 0.0, 0
    if num_features == 1:
        return best_feature
    for i in range(num_features):
        feature_list = [t[i] for t in data_in]
        unique_feature = set(feature_list)
        sub_entropy = 0.0
        for value in unique_feature:
            sub_data_in = split_data_set(data_in, i, value)
            prob = len(sub_data_in)/float(len(data_in))
            sub_entropy += prob * calc_shannon_entropy(sub_data_in)
        info_gain = base_entropy - sub_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature


#
# find out the biggest number presented label in labels
#
def majority_count(labels):
    label_count = {}
    for t in labels:
        if t not in label_count:
            label_count[t] = 1
        else:
            label_count[t] += 1
    sorted_label_count = sorted(label_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_label_count[0][0]


if __name__ == '__main__':
    training_data = np.array([[1, 2, 3], [3, 2, 4], [5, 2, 0]])
    training_label = ["up", "down", "down"]
    data_in = [4, 4, 4]
    print "kNN result:", classify0(data_in, training_data, training_label, 3)

    data_in = [[[1,1,'yes'], [1,0,'no' ], [0,1,'no' ], [0,1,'no' ]], [[1,1,'yes'], [1,0,'no'], [0,1,'no'], [0,1,'no'], [1,0,'maybe']]]
    for data in data_in:
        print "shannon entropy: ", calc_shannon_entropy(data)
        print split_data_set(data, 0, 1)
        print "best feature for shannon entropy: ", choose_best_feature_for_best_shannon_entropy(data)

