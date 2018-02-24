# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import markdown
import codecs
import json

'''
对出版杂志进行分类存储,并生成目录json,方便转换成电子书
2018.2.22
'''

# 保存文件的路径
SAVE_DIR = '/Users/fred/PycharmProjects/economist/'

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Sogousearch/Ios/5.9.8'
}


def markdownTohtml(in_file):
    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)
    print(html)
    return html


def get_article_content(article_url, save_dir):
    '''
    获取单篇文章内容
    :param artical_url: 文章路径
    :param save_dir: 保存路径
    :return:
    '''

    r = requests.get(article_url, headers=headers)

    # print(r.status_code)

    # print(r.text)

    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    # print(soup.prettify())

    # flytitle-and-title__flytitle 小标题获取 20180209
    flytitle_and_title__flytitle = soup.find("span", class_="flytitle-and-title__flytitle")

    # flytitle-and-title__title 标题
    flytitle_and_title_title = soup.find("span", class_="flytitle-and-title__title")

    # 保存的文件路径
    file_path = '{}/{}.md'.format(save_dir, flytitle_and_title_title.get_text())

    file_name = flytitle_and_title_title.get_text()

    f = open(file_path, 'w')

    f.write("###### {}".format(flytitle_and_title__flytitle.get_text()))
    f.write("\n\r")

    f.write("# {}".format(flytitle_and_title_title.get_text()))
    f.write("\n\r")

    print("开始下载文章:{}".format(flytitle_and_title_title.get_text()))

    # blog-post__rubric 子标题
    post_rubric = soup.find("p", class_="blog-post__rubric")

    if post_rubric != None:
        f.write("##### {}".format(post_rubric.get_text()))
        f.write("\n\r")

    # 获取图片
    component_image_img = soup.find("img", class_="component-image__img blog-post__image-block")
    # 文件保存路径
    image_save_path = ''
    image_name = ''
    if component_image_img != None:
        # print(component_image_img.get('src'))
        jpg_src = component_image_img.get('src')

        url_path, img_name = os.path.split(jpg_src)

        # print(img_name)

        # print('{}/images/{}'.format(save_dir,img_name))

        image_save_path = '{}/images/{}'.format(save_dir, img_name)
        image_name = img_name


        with open(image_save_path, 'wb') as file:
            file.write(requests.get(jpg_src).content)

        f.write("![image](images/{})".format(img_name))

        f.write("\n\r")

    # blog-post__section-link 文章分类
    blog_post__section_link = soup.find("a", class_="blog-post__section-link")

    # blog-post__datetime 时间
    blog_post__datetime = soup.find("time", class_="blog-post__datetime")

    if blog_post__section_link != None and blog_post__datetime != None:

        f.write("> {} | {}".format(blog_post__section_link.get_text().replace('print-edition icon ', ''),
                                   blog_post__datetime.get_text()))
        f.write("\n\r")

    elif blog_post__section_link != None:

        f.write("> {}".format(blog_post__section_link.get_text().replace('print-edition icon ', '')))
        f.write("\n\r")

    elif blog_post__datetime != None:
        f.write("> {}".format(blog_post__datetime.get_text()))
        f.write("\n\r")

    # 获取文章内容
    blog_post_text = soup.find("div", class_="blog-post__text")

    #清除订阅邮箱信息
    inbox_newsletter = blog_post_text.find('div', class_='newsletter-form newsletter-form--inline')
    if inbox_newsletter!= None:
        inbox_newsletter.decompose()

    #读取文章
    for p in blog_post_text.find_all('p'):

        if p.get('class') == ['xhead']:  # 20190209 添加内容中子标题
            f.write("##### {}".format(p.get_text()))
            f.write("\n\r")
        elif p.get('class') == None:
            f.write(p.get_text())
            f.write("\n\r")

    # f.write("Power by Fredliu (http://blog.qzcool.com)")
    # f.write("\n\r")

    f.close()

    return file_name, image_name

    print("文章下载完成")


def mkdir(path):
    '''
    创建文件夹目录
    :param path:
    :return:
    '''
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path + ' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def get_print_edition(edition_number):
    '''
    获取期刊内容
    :param edition_number: 刊物版本日期 2018-02-03
    :return:
    '''

    r = requests.get('https://www.economist.com/printedition/{}'.format(edition_number), headers=headers)

    # print(r.status_code)

    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    # print(soup.prettify())

    # 创建文件目录
    # 保存文章的路径
    article_dir = "{}/{}".format(SAVE_DIR, edition_number)
    # 保存图片的目录
    image_dir = "{}/{}/images".format(SAVE_DIR, edition_number)

    mkdir(article_dir)
    mkdir(image_dir)

    # 获取封面图片 component-image__img print-edition__cover-widget__image
    print_edition__cover_widget__image = soup.find("img",
                                                   class_="component-image__img print-edition__cover-widget__image ")
    # print(print_edition__cover_widget__image.get('srcset'))
    cover_widget__images = print_edition__cover_widget__image.get('srcset').split(',')[-1]
    # print(cover_widget__images.split(' ')[0])
    cover_widget__image_url = "{}{}".format("https://www.economist.com",
                                            cover_widget__images.split(' ')[0].replace('\n', '').replace('\r', ''))
    #print(cover_widget__image_url)

    with open('{}/{}'.format(article_dir, "cover.jpg"), 'wb') as file:
        file.write(requests.get(cover_widget__image_url).content)

    # return

    #保存文章路径信息
    json_articale = {}
    json_articale['cover_img'] = "cover.jpg"
    json_articale['edition'] = edition_number

    json_articale['list'] = []

    for list__item in soup.find_all("li", class_="list__item"):
        # print(list__item)
        # 主题标题
        list__title = list__item.find("div", class_="list__title")

        if list__title != None:
            print(list__title.get_text())
        else:
            break

        article_dir_list_title = "{}/{}/{}".format(SAVE_DIR, edition_number, list__title.get_text())
        image_dir_list_title = "{}/{}/{}/images".format(SAVE_DIR, edition_number, list__title.get_text())
        mkdir(article_dir_list_title)
        mkdir(image_dir_list_title)

        json_list__item = {}
        json_list__item['list__title'] = list__title.get_text()
        json_list__item['list__item'] = []

        for article_link in list__item.find_all("a", class_="link-button list__link"):
            print("正在下载文章{}".format(article_link.get('href')))

            file_name, image_name = get_article_content('https://www.economist.com{}'.format(article_link.get('href')),
                                            article_dir_list_title)
            #print(file_path)
            #print(image_save_path)
            # html = markdownTohtml(file_path)
            # print(html)

            list__link = {'list__link': file_name,"articale_image":image_name}
            json_list__item['list__item'].append(list__link)

            #break
        #
        json_articale['list'].append(json_list__item)

    #保存json信息
    with open('{}/{}'.format(article_dir, "economist.json"), 'wb') as file:
        file.write(json.dumps(json_articale).encode())

if __name__ == '__main__':
    get_print_edition('2018-02-24')


    #
    # json_articale = {}
    # json_articale['cover_img'] = "cover.img"
    # json_articale['edition'] = '2018-02-17'
    #
    # json_articale['list'] = []
    #
    # json_list__item = {}
    # json_list__item['list__title'] = 'The world this week'
    # json_list__item['list__item'] = []
    #
    # list__link = {'list__link': 'Detente on the Korean peninsula is a relief.md'}
    # # list__link['list__link'] = 'Detente on the Korean peninsula is a relief.md'
    #
    # json_list__item['list__item'].append(list__link)
    #
    # json_articale['list'].append(json_list__item)
    #
    # print(json_articale)
    # article_dir = "{}/{}".format(SAVE_DIR, '2018-02-17')
    # with open('{}/{}'.format(article_dir, "economist.json"), 'wb') as file:
    #     file.write(json.dumps(json_articale).encode())

        # json_txt['list']['list__item'] = []
        # json_txt['list']['list__item']['list__title'] = 'The world this week'
        # print(json_txt)
