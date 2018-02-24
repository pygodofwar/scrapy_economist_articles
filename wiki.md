
### 从零开始使用BeautifulSoup进行爬网实践

本文使用Python 3进行讲解

安装BeautifulSoup

```python
pip install beautifulsoup4
```
如果你是Python2.7的用下面方式安装:

```python
pip install beautifulsoup
```


#### 1.遍历子节点

假设网页的结构如下,需要抓取文章内容.

```html

<div class="blog-post__text">

<p>some text 1</p>
<p>some text 2</p>
<p>some text 3</p> 
.... 
<figure>
<img src = "/static/some_image.jpg">
</figure>

<p>some text 4</p> 

<p>some text 5</p>

</div>
```

文章内容包含在div中,<p>节点中包含文章内容,其中还穿插图片,为了把文章内容和图片全部抓取出来,需要逐个节点元素进行判断.

```python

# 获取文章内容
blog_post_text = soup.find("div", class_="blog-post__text")
#新增获取文章内部图片
for children in blog_post_text.children: 
    #print(children.name)
    #print(children.attrs)
    if children.name == 'p':
        print(children.string) #获取p内部内容
    if children.name == 'figure':
        #下载文章内部图片
        image_inline = children.find('img')
        
```