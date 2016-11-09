# -*- coding: utf-8 -*-
#
# lhq@python279.org
#


import os
from mydir import mydir
from stock import Stock
import pprint


if __name__ == '__main__':
    s = Stock()
    all_data = s.reload_all()
    pprint.PrettyPrinter().pprint(all_data)
