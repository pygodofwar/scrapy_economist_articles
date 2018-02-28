# -*- coding: UTF-8 -*-

from scrapy_sort_by_type import get_print_edition
from epub_gen import makeEpub

if __name__ == '__main__':

    edition = 'remark/2018-02-24' # 版本信息
    #get_print_edition(edition) # 抓取经济学人文章生成markdown格式文章
    makeEpub(edition) # 生成电子书
