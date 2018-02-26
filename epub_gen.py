#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 生成epub格式电子书

import sys
import markdown
import codecs
from epub import *
import json
import hashlib

SRC_DIR = '/Users/fred/PycharmProjects/economist/' #读取目录
DEST_DIR = '/Users/fred/PycharmProjects/economist/' #保存的目标目录

def MD5(in_string):
    if in_string == None:
        return None
    return hashlib.md5(in_string.encode('utf-8')).hexdigest()

def markdownTohtml(in_file):
    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)
    #print(html)
    return html


def loadHtmlTempler(templer_name, **kwargs):
    tmpl = TemplateLoader('templates').load(templer_name)
    stream = tmpl.generate(**kwargs)
    return stream.render('xhtml', doctype='xhtml11', drop_xml_decl=False)


def makeEpub(edition):
    '''

    :param edition: 版本号
    :return:
    '''
    book = EpubBook()

    article_dir = "{}{}".format(SRC_DIR, edition)
    json_articale = {}
    with open('{}/{}'.format(article_dir, "economist.json"), 'rb') as file:
        text_json = file.read()
        json_articale = json.loads(text_json)

    #print(json_articale['cover_img'])
    #print(json_articale['edition'])
    # print(json_articale['list'])


    book.setTitle('The Economist {}'.format(json_articale['edition']))
    book.addCreator('Monkey D Luffy')
    book.addCreator('Guybrush Threepwood')
    book.addMeta('contributor', 'Smalltalk80', role='bkp')
    book.addMeta('date', json_articale['edition'], event='publication')

    book.addTitlePage()
    book.addTocPage()
    book.addCover(r'{}/{}'.format(article_dir, json_articale['cover_img']))

    book.addCss(r'templates/stylesheet.css', 'stylesheet.css')
    book.addCss(r'templates/page_styles.css', 'page_styles.css')

    topics = []

    for list_items in json_articale['list']:
        topics.append(list_items['list__title'])



    n1 = book.addHtml('', 'topic.html', loadHtmlTempler('topic.html', deition=json_articale['edition'], topics=topics))
    book.addSpineItem(n1)
    # book.addTocMapNode(n1.destPath, '1')


    for index, list_items in enumerate(json_articale['list']):
        #print(list_items['list__title'])
        #print(index)

        topic = list_items['list__title']

        articles = []

        for list_item in list_items['list__item']:
            articles.append((MD5(list_item['list__link']),list_item['list__link']))

        # 下一主题
        if index + 1 < len(json_articale['list']):
            next_topic = json_articale['list'][index + 1]['list__title']
        else:
            next_topic = json_articale['list'][0]['list__title']

        # 上一个主题
        Previous_section = None

        if index > 0:
            Previous_section = json_articale['list'][index - 1]['list__title']

        book_list_h1 = book.addHtml('', '{}.html'.format(list_items['list__title']),
                                    loadHtmlTempler('sub-topic.html', Previous_section=Previous_section,
                                                    next_topic=next_topic, articles=articles, topic=topic))
        book.addSpineItem(book_list_h1)
        book.addTocMapNode(book_list_h1.destPath, list_items['list__title'])


        for index_item,list_item in enumerate(list_items['list__item']):
            #print(list_item['list__link'])
            #print(list_item['articale_image'])

            #拷贝文章图片,支持多图片
            if list_item['articale_image'] != []:
                for image_item in list_item['articale_image']:
                    book.addImage(
                        "{}/{}/images/{}".format(article_dir, list_items['list__title'], image_item),
                        "images/{}".format(image_item))


            title = list_item['list__link']
            content = markdownTohtml("{}/{}/{}.md".format(article_dir,list_items['list__title'],list_item['list__link']))

            Previous = None
            next_item = None

            if index_item >0:
                Previous =  list_items['list__item'][index_item-1]['list__link']

            if index_item+1 < len(list_items['list__item']):
                next_item = list_items['list__item'][index_item+1]['list__link']

            #print(urllib.parse.quote_plus(list_item['list__link']))


            node_articale = book.addHtml('', '{}.html'.format(MD5(list_item['list__link'])),
                                         loadHtmlTempler('article-content.html', Previous=MD5(Previous),
                                                         next=MD5(next_item),Section_menu = topic, content=content,title = title, topic=topic))

            book.addSpineItem(node_articale)
            book.addTocMapNode(node_articale.destPath, list_item['list__link'], 2)



    rootDir = r'{}The Economist {}'.format(DEST_DIR,json_articale['edition'])
    book.createBook(rootDir)
    EpubBook.createArchive(rootDir, rootDir + '.epub')


if __name__ == '__main__':

    makeEpub('2018-02-24')
    #makeEpub('2018-02-17')
