# -*- coding: UTF-8 -*-

from scrapy_sort_by_type import get_print_edition
from epub_gen import makeEpub

if __name__ == '__main__':

    edition = '2018-02-24'
    #get_print_edition('2018-02-24')
    makeEpub(edition)
    # L = [('spam1', 'Spam11'), ('spam2', 'Spam22')]
    # L.append(('spam3','spam33'))
    #
    # for l in L:
    #     print(l[0])
    #     print(l[1])