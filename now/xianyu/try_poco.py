# -*- encoding=utf8 -*-
__author__ = "MI"

import re
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


def wait_ui_childeren(*args, **kwargs):
    try:
        poco(*args, **kwargs).wait_for_appearance(timeout=3)
    except PocoTargetTimeout:
        return []
    else:
        return poco(*args, **kwargs).children()


def scroll_screen(pos1=None, pos2=None, duration=0.6):
    if pos1 is None:
        poco.swipe([0.5, 0.7], [0.5, 0.3], duration=duration)
    elif isinstance(pos1, UIObjectProxy):
        pos1 = pos1.get_position()
        pos2 = pos2.get_position()
        poco.swipe(list(pos1), list(pos2), duration=duration)
    elif isinstance(pos1, list):
        poco.swipe(pos1, pos2, duration=duration)


def judge_where():
    result_obj = poco('android.widget.ScrollView').children()
    for result in result_obj:
        if '人想要 ·' in result.get_text():
            return True


def get_up_info():
    # result_obj = poco('android.widget.ScrollView').child(
    #     "android.widget.FrameLayout")
    # result_obj = poco(text='宝贝视频').sibling()
    sign = None
    result_obj = wait_ui_childeren('android.widget.ScrollView')
    for index, result in enumerate(result_obj):
        # sign = result(textMatches='.*\n.*发布于.*')
        text = result.get_text()
        if re.search(r'.*\n.*发布于.*', text):
            sign = index
            break

    if sign is None:
        return {}

    info = {}
    info['个人信息'] = result_obj[sign].get_text()
    info['售价'] = result_obj[sign + 1].get_text()
    info['商品介绍'] = result_obj[sign + 2].get_text()
    try:
        info['商品介绍2'] = result_obj[sign + 3].get_text()
    except Exception:
        info['商品介绍2'] = None

    return info


def get_comment(item):
    result_obj = item.children()
    if len(result_obj) == 3:
        text = item.get_text()
        name = result_obj[2].get_text()
        return {name: text}
    elif len(result_obj) == 2:
        comment = []
        for result in result_obj:
            comment.append(get_comment(result))
        return comment


def get_down_info():
    info = {}
    info['留言'] = []
    info['添加时间'] = time.time()

    result_obj = wait_ui_childeren('android.widget.ScrollView')
    while '人想要 ·' not in result_obj[0].get_text():
        scroll_screen([0.4, 0.42], [0.5, 0.52], duration=1)
        result_obj = wait_ui_childeren('android.widget.ScrollView')
        if result_obj[0].get_text() is None:
            break
    # while True:
    for index, result in enumerate(result_obj):
        text = result.get_text()
        if text:
            if re.search('.*\n来闲鱼[1-9]\d*天了[\s\S]*', text):
                info['个人简介'] = text
            elif re.search('^全部留言.*$', text):
                info['留言个数'] = text
            elif re.search('[\s\S]*人想要[\s\S]*超赞[\s\S]*浏览[\s\S]*', text):
                info['人数'] = text
        elif len(result.children()) != 0:
            comment = get_comment(result)
            if comment not in info['留言']:
                info['留言'].append(comment)
        # if len(info['留言']) >= 6:
        #     break
        # scroll_screen([0.4, 0.42], [0.5, 0.3], duration=1)
        # result_obj = wait_ui_childeren('android.widget.ScrollView')

    return info


def find_ui():
    retry = 5
    result = None
    while retry:
        try:
            result = poco(textMatches='^全部留言.*$')
            return result
        except PocoNoSuchNodeException:
            retry -= 1
            scroll_screen([0.4, 0.42], [0.5, 0.52], duration=1)


def level_page():
    info = run_func(get_up_info)

    if info:
        while True:
            try:
                poco(textMatches='^全部留言.*$').wait_for_appearance(timeout=1)
            except PocoTargetTimeout:
                scroll_screen()
            except Exception as exc:
                print(exc)
            else:
                pos = find_ui().get_position()
                scroll_screen(pos, [0.5, 0.3], duration=3)
                down_info = run_func(get_down_info)
                if down_info:
                    info.update(down_info)
                    with open('./data.txt', 'a', encoding='utf-8') as fn:
                        fn.write(json.dumps(info, ensure_ascii=False))
                        fn.write('\n')
                break

    # while not judge_where():
    #     for child in poco('android.widget.ScrollView').children():
    #         pos = child.get_position()
    #         for _ in pos:
    #             if _ > 0.9 or _ < 0.1:
    #                 continue
    #             else:
    #                 pass
    #     poco()
    #     scroll_screen()


def outside():
    while True:
        result_obj = poco("com.taobao.idlefish:id/weex_render_view").offspring(
            "android.support.v7.widget.RecyclerView").child(
                "android.widget.FrameLayout")

        if len(result_obj) != 6:
            print('obj lenght error')
        else:
            for index in [1, 4]:
                result_obj[index].click('center')
                level_page()
                poco(text="返回").click()

        scroll_screen(result_obj[3], result_obj[1])


if __name__ == "__main__":
    while True:
        run_func(outside)
    # outside()
    # level_page()
    # get_up_info()
    # get_down_info()
