class PageInfo():
    """
    :param current_page: 当前页码
    :param all_count: 数据库总行数
    :param per_page: 每页显示行数
    :param base_url: 基本路径
    :param show_page: 每页显示页码数

    """

    def __init__(self, current_page, all_count, per_page, base_url, show_page=11):
        # 防止页面的非法输入
        try:
            self.current_page = int(current_page)
        except Exception as e:
            # 非法输入时跳到首页
            self.current_page = 1
        self.per_page = per_page

        a, b = divmod(all_count, per_page)
        if b:
            a = a + 1
        self.all_pager = a  # 数据总共有多少页
        self.show_page = show_page  # 每页显示的 页码 数
        self.base_url = base_url

    def start(self):
        return (self.current_page - 1) * self.per_page

    def end(self):
        return self.current_page * self.per_page

    def pager(self):
        page_list = []

        # 页码中间值
        half = int((self.show_page - 1) / 2)

        # 如果数据总页数 < 11 页
        if self.all_pager < self.show_page:
            begin = 1
            stop = self.all_pager + 1
        # 如果数据总页数>11页
        else:
            # 如果当前页 <=5，永远显示1-11页
            if self.current_page <= half:
                begin = 1
                stop = self.show_page + 1
            else:
                # 当前页+5，超出了总页数
                if self.current_page + half > self.all_pager:
                    begin = self.all_pager - self.show_page + 1
                    stop = self.all_pager + 1
                else:
                    # 正常显示页码
                    begin = self.current_page - half
                    stop = self.current_page + half + 1

        # 上一页
        if self.current_page <= 1:
            prev = "<li><a href='#'>上一页</a1></li>"
        else:
            prev = "<li><a href='%s?page=%s'>上一页</a1></li>" % (self.base_url, self.current_page - 1)
        page_list.append(prev)

        # 页码
        for i in range(begin, stop):
            if i == self.current_page:
                page_list.append("<li class='active'><a href='%s?page=%s'>%s</a1></li>" % (self.base_url, i, i))
            else:
                page_list.append("<li><a href='%s?page=%s'>%s</a1></li>" % (self.base_url, i, i))

        # 下一页
        if self.current_page >= self.all_pager:
            after = "<li><a href='#'>下一页</a></li>"
        else:
            after = "<li><a href='%s?page=%s'>下一页</a></li>" % (self.base_url, self.current_page + 1)
            page_list.append(after)
        return "".join(page_list)