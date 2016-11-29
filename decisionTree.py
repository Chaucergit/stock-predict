# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


from dataProcess import *


class DecisionTree():
    def __init__(self, data_in, labels):
        self.data_in = data_in
        self.labels = labels
        self.my_tree = None

    def __del__(self):
        pass

    def get_my_tree(self):
        if not self.my_tree:
            self.create_tree()
        return self.my_tree

    def create_tree(self):
        data_in = self.data_in
        labels = self.labels[:] # copy the labels since it will be changed in _create_tree

        def _create_tree(data_in, labels):
            class_list = [t[-1] for t in self.data_in]
            # no difference class in left data_in, just return the class
            if class_list.count(class_list[0]) == len(class_list):
                return class_list[0]
            # return the largest presented class when no left feature in data_in
            if len(data_in[0]) == 1:
                return majority_count(class_list)
            # choose the best feature as the high priority one with best shannon entropy
            best_feature = choose_best_feature_for_best_shannon_entropy(data_in)
            best_feature_label = labels[best_feature]
            my_tree = {best_feature_label:{}}
            del labels[best_feature]
            feature_values = [t[best_feature] for t in data_in]
            unique_values = set(feature_values)
            # traverse all the values of the best feature
            for value in unique_values:
                sub_labels = labels[:] # copy the list
                my_tree[best_feature_label][value] = _create_tree(split_data_set(data_in, best_feature, value), sub_labels)
            return my_tree

        self.my_tree = _create_tree(data_in, labels)

    def classify(self, test_vector):
        if not self.my_tree:
            self.create_tree()

        def _classify(my_tree, labels, test_vector):
            first_label = my_tree.keys()[0]
            next_dict = my_tree[first_label]
            feature_index = labels.index(first_label)
            if type(next_dict[test_vector[feature_index]]) == dict:
                class_label = _classify(next_dict[test_vector[feature_index]], labels, test_vector)
            else:
                class_label = next_dict[test_vector[feature_index]]
            return class_label

        return _classify(self.my_tree, self.labels, test_vector)


if __name__ == '__main__':
    data_in = [[1,1,'yes'], [1,0,'no'], [0,1,'no'], [0,1,'no'], [1,0,'maybe']]
    labels = ["A", "B"]
    dt = DecisionTree(data_in, labels)
    print dt.get_my_tree()
    print dt.classify([1,1])
    print dt.classify([1,0])
    print dt.classify([0,1])
