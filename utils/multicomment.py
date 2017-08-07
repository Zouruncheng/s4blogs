def comment_tree(comment_list):
    comment_str = "<div class='comment'>"
    for item in comment_list:
        tpl = "<div class='content'>%s</div>" %(item["content"])
        comment_str += tpl
        if item["child"]:
            child_str = comment_tree(item["child"])
            comment_str += child_str
    comment_str += "</div>"
    return comment_str