# -*- coding: UTF-8 -*-

from scrapy_sort_by_type import get_print_edition
from epub_gen import makeEpub

if __name__ == '__main__':

    edition = '2018-02-24'
    #get_print_edition('2018-02-24')
    makeEpub(edition)
