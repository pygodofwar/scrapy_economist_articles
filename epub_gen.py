# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import markdown
import codecs
import json

'''
生成epub格式电子书
'''

SAVE_DIR = '/Users/fred/PycharmProjects/economist/'

if __name__ == '__main__':

    article_dir = "{}/{}".format(SAVE_DIR, '2018-02-17')
    json_articale = {}
    with open('{}/{}'.format(article_dir, "economist.json"), 'rb') as file:
        text_json = file.read()
        #print(text_json)

        json_articale =  json.loads(text_json)

    print(json_articale['cover_img'])

    print(json_articale['list'])