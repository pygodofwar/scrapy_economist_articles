# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os

'''
使用爬虫获取经济学人期刊文章,自动保存成markdown格式,可以使用MWeb等markdown工具编辑方便阅读或者转换成word,pdf格式
2018-02-07
blog.qzcool.com
by fredliu
'''

#保存文件的路径
SAVE_DIR = '/Users/fred/PycharmProjects/economist/'

headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Sogousearch/Ios/5.9.8'
    }


def get_article_content(article_url,save_dir):
    '''
    获取单篇文章内容
    :param artical_url: 文章路径
    :param save_dir: 保存路径
    :return:
    '''

    r = requests.get(article_url, headers=headers)

    #print(r.status_code)

    #print(r.text)

    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    #print(soup.prettify())

    # flytitle-and-title__flytitle 小标题获取 20180209
    flytitle_and_title__flytitle = soup.find("span", class_="flytitle-and-title__flytitle")

    # flytitle-and-title__title 标题
    flytitle_and_title_title = soup.find("span", class_="flytitle-and-title__title")

    f = open('{}/{}.md'.format(save_dir,flytitle_and_title_title.get_text()), 'w')

    f.write("###### {}".format(flytitle_and_title__flytitle.get_text()))
    f.write("\n\r")

    f.write("# {}".format(flytitle_and_title_title.get_text()))
    f.write("\n\r")

    print("开始下载文章:{}".format(flytitle_and_title_title.get_text()))

    #blog-post__rubric 子标题
    post_rubric = soup.find("p", class_="blog-post__rubric")

    if post_rubric != None:

        f.write("##### {}".format(post_rubric.get_text()))
        f.write("\n\r")



    #获取图片
    component_image_img= soup.find("img", class_="component-image__img blog-post__image-block")

    if component_image_img != None:
        #print(component_image_img.get('src'))
        jpg_src = component_image_img.get('src')

        url_path, img_name = os.path.split(jpg_src)

        #print(img_name)

        #print('{}/images/{}'.format(save_dir,img_name))

        with open('{}/images/{}'.format(save_dir,img_name), 'wb') as file:
            file.write(requests.get(jpg_src).content)

        f.write("![image](images/{})".format(img_name))

        f.write("\n\r")


    # blog-post__section-link 文章分类
    blog_post__section_link = soup.find("a", class_="blog-post__section-link")


    #blog-post__datetime 时间
    blog_post__datetime = soup.find("time", class_="blog-post__datetime")

    if blog_post__section_link != None and blog_post__datetime != None:

        f.write("> {} | {}".format(blog_post__section_link.get_text().replace('print-edition icon ',''),blog_post__datetime.get_text()))
        f.write("\n\r")

    elif blog_post__section_link != None:

        f.write("> {}".format(blog_post__section_link.get_text().replace('print-edition icon ', '')))
        f.write("\n\r")

    elif blog_post__datetime != None:
        f.write("> {}".format(blog_post__datetime.get_text()))
        f.write("\n\r")

    #获取文章内容
    blog_post_text = soup.find("div", class_="blog-post__text")

    # 清除订阅邮箱信息
    inbox_newsletter = blog_post_text.find('div', class_='newsletter-form newsletter-form--inline')
    if inbox_newsletter!= None:
        inbox_newsletter.decompose()

    for p in blog_post_text.find_all('p'):

        if p.get('class') == ['xhead']: # 20190209 添加内容中子标题
            f.write("##### {}".format(p.get_text()))
            f.write("\n\r")
        elif p.get('class') == None:
            f.write(p.get_text())
            f.write("\n\r")

    #f.write("Power by Fredliu (http://blog.qzcool.com)")
    #f.write("\n\r")

    f.close()

    print("文章下载完成")

def get_tpoics_articles(topics_url):
    '''
    获取专题文章
    :param topics_url: https://www.economist.com/latest-updates
    :return:
    '''

    # 创建topic目录
    url_path, topic_name = os.path.split(topics_url)
    # 保存文章的路径
    article_dir = "{}/{}".format(SAVE_DIR, topic_name)
    # 保存图片的目录
    image_dir = "{}/{}/images".format(SAVE_DIR, topic_name)

    mkdir(article_dir)
    mkdir(image_dir)

    r = requests.get(topics_url, headers=headers)
    #print(r.status_code)

    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    #print(soup.prettify())

    #获取文章链接
    for article_teaser in soup.find_all("article", class_="teaser"):

        #print(article_teaser.prettify())

        article_link = article_teaser.find("a")

        print("正在下载文章{}".format(article_link.get('href')))

        get_article_content('https://www.economist.com{}'.format(article_link.get('href')), article_dir)


def get_print_edition(edition_number):
    '''
    获取期刊内容
    :param edition_number: 刊物版本日期 2018-02-03
    :return:
    '''

    r = requests.get('https://www.economist.com/printedition/{}'.format(edition_number), headers=headers)

    #print(r.status_code)

    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    #print(soup.prettify())

    #创建文件目录
    #保存文章的路径
    article_dir = "{}/{}".format(SAVE_DIR,edition_number)
    #保存图片的目录
    image_dir = "{}/{}/images".format(SAVE_DIR,edition_number)

    mkdir(article_dir)
    mkdir(image_dir)

    for article_link in soup.find_all("a", class_="link-button list__link"):

        print("正在下载文章{}".format(article_link.get('href')))

        get_article_content('https://www.economist.com{}'.format(article_link.get('href')),article_dir)


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

if __name__ == '__main__':

    artical_url ='https://www.economist.com/news/china/21737069-party-wants-people-rent-china-trying-new-ways-skimming-housing-market-froth'
    get_article_content(artical_url,'/Users/fred/PycharmProjects/economist')
    #pass

    #get_print_edition('2018-02-03')
    #get_tpoics_articles('https://www.economist.com/latest-updates')






