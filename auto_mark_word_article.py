# -*- coding: UTF-8 -*-
import codecs
from stardict import *
import commFun as comm
from shutil import copyfile

'''
对文章单词自动标识
'''

# 保存文件的路径
article_dir_src = '/Users/fred/PycharmProjects/economist/'

sqlite_name = os.path.join(os.path.dirname(__file__), 'ecdict.sqlite')

sd = StarDict(sqlite_name)

# 单词标签,要过滤的单词标签

WORD_TAG = set(['gk', 'zk', 'cet4'])



def getLemma(word):
    # 获取单词的原形
    word_rs = sd.query(word)

    if word_rs == None:
        return None

    exchange = word_rs.get('exchange')

    if exchange == '':
        return None

    exchanges = exchange.split('/')

    dic = {}
    for ex in exchanges:
        elem = ex.split(':')
        dic[elem[0]] = elem[1]

    if '0' in dic.keys():
        return dic['0']
    else:
        return None


def searchWord(word):
    # 对单词难度进行分类,低于以下的不返还回结果


    word_rs = sd.query(word)

    if word_rs == None:
        return None

    # print(word_rs)
    # print('\r')
    # print("tag: {}".format(word_rs.get('tag')))

    tags = set(word_rs.get('tag').split(' '))
    # print(tags)
    # print(tags - WORD_TAG)

    if len(tags - WORD_TAG) != len(tags):
        return None

    #return "{}[{}]:definition:{}\ntranslation:{} ".format(word_rs.get('word'), word_rs.get('phonetic'),
    #                                                      word_rs.get('definition'), word_rs.get('translation'))

    return "{}[{}]:{} ".format(word_rs.get('word'), word_rs.get('phonetic'), word_rs.get('translation').replace('\n',' '))


def replaceChars(text, chars):
    for char in chars:
        text = text.replace(char, '')
    return text


def passed(item):
    # 清除介词和常见单词,数字
    # 介词
    prep_word = ['i', 'his', 'they', 'then', 'their', 'on', 'is', 'are', 'was', 'of', 'at', 'and', 'this', 'In', 'a',
                 'an', 'in', 'as', 'not', 'the', 'but', 'from', 'to', 'will',
                 'who', 'he', 'up', 'by', 'has', 'have', 'for', 'may', 'does', 'that', 'it', 'its', 'with', 'more',
                 'though', 'under', 'show', 'after', 'set', 'late', 'one', 'two', 'been',
                 'most', 'between', 'first', 'three', 'now', 'name', 'mr', 'english', 'china', 'chinese', 'path',
                 'year', 'no',
                 'she', 'her', 'ms', 'ever', 'too', 'gone', 'might', 'get', 'our', 'so', 'or', 'also', 'some', 'them',
                 'all', 'be',
                 'would', 'where', 'your', 'until', 'buy', 'such', 'could', 'such', 'much', 'only', 'own', 'about',
                 'many', 'add',
                 'seen', 'what', 'other', 'since', 'into', 'unit', 'do', 'these', 'when']

    try:
        # print("{} {}".format(item,item.isalpha()))

        return item.isalpha() and (item.lower() not in prep_word)  # can be more a complicated condition here
    except ValueError:
        return False


def readMarkdownFile(in_file):
    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()

    # 需要过滤的特殊字符
    special_char = ['.', ',', '“', '”', '#', '\r', '\n', '|', '>', ')', '(', ';']

    replace_words = special_char
    # 过滤特殊字符
    words = replaceChars(text, replace_words).split(' ')
    # 过滤常见单词和介词
    words = list(filter(passed, words))

    print(len(words))

    word_set = set()

    translation_txt = ''
    index = 1
    for word in words:

        word_lemma = getLemma(word)

        if word_lemma != None:
            word = word_lemma

        if word in word_set:
            #print("{} 包含在集合里面".format(word))
            continue

        word_set.add(word)


        translation = searchWord(word)
        if translation != None:
            #print(translation)
            translation_txt += "{}.{}\n\r".format(index,translation)
            index = index+1

    print(translation_txt)
    return text+"-- \n\r 单词注释:\n\r"+translation_txt

# 标注后保存的地址
article_remark_dir = '/Users/fred/PycharmProjects/economist/remark'


def remarkEdition(edition):
    '''
    对印刷版进行单词标注
    :param edition:
    :return:
    '''
    article_dir = "{}{}".format(article_dir_src, edition)
    json_articale = {}
    with open('{}/{}'.format(article_dir, "economist.json"), 'rb') as file:
        text_json = file.read()
        json_articale = json.loads(text_json)

        # 创建目录
        comm.mkdir('{}/{}'.format(article_remark_dir, edition))

        with open('{}/{}/{}'.format(article_remark_dir, edition, "economist.json"), 'wb') as file:
            file.write(json.dumps(json_articale).encode())

    # print(json_articale)

    # cover.jpg
    src_cover_image = '{}/cover.jpg'.format(article_dir)
    dst_cover_image = '{}/{}/cover.jpg'.format(article_remark_dir, edition)

    copyfile(src_cover_image, dst_cover_image)

    for list_items in json_articale['list']:
        # topics.append(list_items['list__title'])

        topic = list_items['list__title']
        # print(list_items['list__title'])
        # print(list_items['list__item'])
        file_save_path = '{}/{}/{}'.format(article_remark_dir, edition, topic)
        comm.mkdir(file_save_path)

        dst_image_save_path = '{}/images'.format(file_save_path)
        comm.mkdir(dst_image_save_path)

        for list_item in list_items['list__item']:
            print(list_item['list__link'])

            # 文章标识
            text = readMarkdownFile(
                "{}/{}/{}.md".format(article_dir, topic, list_item['list__link']))

            with open('{}/{}.md'.format(file_save_path, list_item['list__link']), 'w') as file:
                file.write("{}".format(text))

            # 图片拷贝
            for image in list_item['articale_image']:
                src_image = '{}/{}/images/{}'.format(article_dir, list_items['list__title'], image)
                dst_imgae = '{}/{}'.format(dst_image_save_path, image)
                copyfile(src_image, dst_imgae)


if __name__ == '__main__':
    remarkEdition('2018-02-24')


    # text = readMarkdownFile("{}/{}.md".format(article_dir,"China is trying new ways of skimming housing-market froth"))
    #
    # f = open("{}/{}.md".format(article_dir,"test"), 'w')
    # f.write("{}".format(text))
    # f.close()
    # edition = '2018-02-24'
    # article_remark_dir = '/Users/fred/PycharmProjects/economist/remark'
    #
    # article_dir = "{}{}".format(article_dir, edition)
    # json_articale = {}
    # with open('{}/{}'.format(article_dir, "economist.json"), 'rb') as file:
    #     text_json = file.read()
    #     json_articale = json.loads(text_json)
    #
    #     #创建目录
    #     comm.mkdir('{}/{}'.format(article_remark_dir,edition))
    #
    #     with open('{}/{}/{}'.format(article_remark_dir,edition, "economist.json"), 'wb') as file:
    #         file.write(json.dumps(json_articale).encode())
    #
    # #print(json_articale)
    #
    # #cover.jpg
    # src_cover_image = '{}/cover.jpg'.format(article_dir)
    # dst_cover_image = '{}/{}/cover.jpg'.format(article_remark_dir,edition)
    #
    #
    # copyfile(src_cover_image, dst_cover_image)
    #
    #
    #
    # for list_items in json_articale['list']:
    #     #topics.append(list_items['list__title'])
    #
    #     topic = list_items['list__title']
    #     #print(list_items['list__title'])
    #     #print(list_items['list__item'])
    #     file_save_path = '{}/{}/{}'.format(article_remark_dir, edition, topic)
    #     comm.mkdir(file_save_path)
    #
    #     dst_image_save_path = '{}/images'.format(file_save_path)
    #     comm.mkdir(dst_image_save_path)
    #
    #     for list_item in list_items['list__item']:
    #         print(list_item['list__link'])
    #
    #         #文章标识
    #         text = readMarkdownFile(
    #             "{}/{}/{}.md".format(article_dir,topic, list_item['list__link']))
    #
    #         with open('{}/{}.md'.format(file_save_path,  list_item['list__link']), 'w') as file:
    #             file.write("{}".format(text))
    #
    #         # 图片拷贝
    #         for image in list_item['articale_image']:
    #             src_image = '{}/{}/images/{}'.format(article_dir,list_items['list__title'],image)
    #             dst_imgae = '{}/{}'.format(dst_image_save_path,image)
    #             copyfile(src_image, dst_imgae)


            #with open('{}/{}/{}/{}'.format(article_remark_dir,edition, list_items['list__title'],list_item['list__link']), 'w') as file:


    #print(searchWord('mandatory'))


    # print(getLemma('predictability'))

    # crazystring = 'dade142.;!0142'
    #
    # str = list(filter(str.isalpha, crazystring))
    # print( str )

    # def passed(item):
    #     try:
    #         return item != "techbrood"  # can be more a complicated condition here
    #     except ValueError:
    #         return False
    #
    #
    # org_words = ["this" ,"is" ,"demo", "from" ,"techbrood"]
    # #words =  [filter(passed, item) for item in org_words]
    # words = list(filter(passed, org_words))
    #
    # print(words)
    #
    # for word in words:
    #     print(word)
