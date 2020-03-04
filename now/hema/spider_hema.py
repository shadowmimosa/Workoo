import json
import time
from airtest.core.api import *
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoTargetTimeout, PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from config import logger
from utils.run import run_func

poco = AndroidUiautomationPoco(use_airtest_input=True,
                               screenshot_each_action=False)


def comment(obj):
    return obj.offspring('com.wudaokou.hippo:id/tv_comment').get_text()
    # return obj.offspring('com.wudaokou.hippo:id/rl_comments').get_text()


def name(obj):
    # PocoNoSuchNodeException
    return obj.offspring('com.wudaokou.hippo:id/tv_user_name').get_text()


def satisfaction(obj):
    return obj.offspring('com.wudaokou.hippo:id/tv_good_or_bad').get_text()


def date(obj):
    return obj.offspring('com.wudaokou.hippo:id/tv_order_date').get_text()


def parser_comment(obj):
    last = None
    first = None
    try:
        obj.offspring('com.wudaokou.hippo:id/rl_comments').get_text()
    except PocoNoSuchNodeException:
        try:
            obj.offspring('com.wudaokou.hippo:id/image').get_text()
        except PocoNoSuchNodeException:
            return
        else:
            return '图片'

    try:
        last = obj.offspring('com.wudaokou.hippo:id/tv_comment').get_text()
    except PocoNoSuchNodeException:
        pass
    try:
        first = obj.offspring(
            'com.wudaokou.hippo:id/tv_comment_tag').get_text()
    except PocoNoSuchNodeException:
        pass

    if first and last:
        comments = [first, last]
    elif first:
        comments = [first, None]
    elif last:
        comments = [None, last]
    else:
        return None

    return comments


def get_text(obj):
    result = []
    for path in [
            'com.wudaokou.hippo:id/tv_user_name',
            'com.wudaokou.hippo:id/tv_good_or_bad',
            'com.wudaokou.hippo:id/tv_order_date'
    ]:
        try:
            result.append(obj.offspring(path).get_text())
        except PocoNoSuchNodeException:
            return

    result.append(parser_comment(obj))
    result.append(ID)

    return result


def scroll_screen(pos1=None, pos2=None, duration=0.5):
    if pos1 is None:
        poco.swipe([0.5, 0.8], [0.5, 0.3], duration=duration)
    elif isinstance(pos1, UIObjectProxy):
        pos1 = pos1.get_position()
        pos2 = pos2.get_position()
        poco.swipe(list(pos1), list(pos2), duration=duration)
    elif isinstance(pos1, list):
        poco.swipe(pos1, pos2, duration=duration)


def is_repeat(item):
    global LAST
    # if item not in total[-10:]:
    #     return True

    if None in item:
        return True

    return False

    if item[0] == LAST:
        return True
    else:
        LAST = item[0]


def write(content):
    with open(f'./{ID}.txt', 'a', encoding='utf-8') as fn:
        if isinstance(content, list):
            content = json.dumps(content, ensure_ascii=False)

        fn.write(content)
        fn.write('\n')


def detail(child):
    # item = [name(child), comment(child), satisfaction(child), date(child)]
    item = get_text(child)

    if not item:
        return

    write(item) if not is_repeat(item) else True


def main():
    result = poco("com.wudaokou.hippo:id/rv_comments_list").child(
        "android.widget.LinearLayout")

    while result:
        for child in result:
            detail(child)

        scroll_screen()
        time.sleep(1)
        result = poco("com.wudaokou.hippo:id/rv_comments_list").child(
            "android.widget.LinearLayout")


LAST = ''
ID = 9

if __name__ == "__main__":
    main()