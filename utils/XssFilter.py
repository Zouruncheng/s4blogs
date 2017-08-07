# pip3 install beautifulsoup4
from bs4 import BeautifulSoup
def xss(old):
    """
    防范xss攻击，过滤关键字符串。
    :param old: 用户提交的博文内容或字符串
    :return: new_str,返回合法的字符
    """
    valid_tags = {
        "font": ['color', 'size', 'face', 'style'],
        'b': [],
        'div': [],
        "span": [],
        "table": [
            'border', 'cellspacing', 'cellpadding'
        ],
        'th': [
            'colspan', 'rowspan'
        ],
        'td': [
            'colspan', 'rowspan'
        ],
        "a": ['href', 'target', 'name'],
        "img": ['src', 'alt', 'title'],
        'p': [
            'align'
        ],
        "pre": ['class'],
        "hr": ['class'],
        'strong': [],
        "h1":[],
        "h2":[],
        "h3":[],
        "h4":[],
        "h5":[],
        "P":[],
    }

    soup = BeautifulSoup(old, "html.parser")
    # 找到所有标签
    tags = soup.find_all()
    for tag in tags:
        if tag.name not in valid_tags:
            # 删除该标签对象
            tag.decompose()
            # tag.clean() # 删除标签内容
        if tag.attrs:
            # 循环标签的属性
            for i in list(tag.attrs.keys()):
                if i not in valid_tags[tag.name]:
                    del tag.attrs[i]
    content_str = soup.decode()
    return content_str


