import time
import sys
import re
from xml.etree import ElementTree as ET

from django.utils.encoding import smart_str
from django.db.utils import IntegrityError
from wechat.models import UserInfo, TransactionInfo
from wechat.utils.service import DealService
from wechat.utils.common import get_event
from wechat.tasks import main
from query_service.mycelery import app

# from now.wx_service.wechat.tasks import main
# from now.wx_service.query_service.mycelery import app
# from now.wx_service.wechat.utils.service import DealService
# from now.wx_service.wechat.models import UserInfo, TransactionInfo

event_list = get_event()


class Analysis:
    def __init__(self, xmlData):
        print("接收到的数据：" + xmlData)
    
    def judge_imei(self,content):
        # sn_pattern = re.compile(r"^[0-9a-zA-Z]{11,12}$")
        # imei_pattern = re.compile(r"^[0-9]{15}$")
        # imei = re.match(r"^[0-9]{15}$",content)
        if re.match(r"^[0-9]{15}$",content) != None:
            return content
        elif re.match(r"^[0-9a-zA-Z]{11,12}$",content)!=None:
            return content
        else:
            return
        # sn = re.match(r"^[0-9a-zA-Z]{11,12}$",content)

    def prase(self, xmlText):
        xmlData = ET.fromstring(xmlText)
        msgType = xmlData.find("MsgType").text
        toUserName = xmlData.find("ToUserName").text
        fromUserName = xmlData.find("FromUserName").text

        if msgType == 'text':
            openid = xmlData.find("FromUserName").text
            content = xmlData.find("Content").text
            try:
                current = UserInfo.objects.query_current(openid)
            except UserInfo.DoesNotExist:
                reply_content = "请在菜单栏选择要查询的项目"
            else:
                # imei = xmlData.find("Content").text
                imei = self.judge_imei(content)
                if imei!=None:
                    if sys.platform == "win32":
                        reply_content = DealService(
                            openid=openid, current=current, imei=imei).main()
                    else:
                        reply_content = "爱锋妹正在为您查询中····· \n注意：请勿重复提交信息 \n如超过5分钟未出结果请联系客服 315523827"
                        main.delay(toUserName, openid, current, imei)
                else:
                    reply_content = "请输入正确的 IMEI 或 SN"

            TextMsgObj = TextMsg(toUserName, fromUserName, reply_content)
            return TextMsgObj.structReply()

        elif msgType == 'image':
            mediaId = xmlData.find("MediaId").text

            ImageMsgObj = ImageMsg(toUserName, fromUserName, mediaId)
            return ImageMsgObj.structReply()

        elif msgType == 'event':
            openid = xmlData.find("FromUserName").text
            eventKey = xmlData.find("EventKey").text

            try:
                UserInfo.objects.insert_user(openid, current=eventKey)
            except IntegrityError as exc:
                if exc.args[0] == 1062 and "Duplicate entry" in exc.args[1]:
                    UserInfo.objects.update_current(openid, eventKey)
                    return TextMsg(toUserName, fromUserName,
                                   "请在菜单栏选择要查询的项目").structReply()
                else:
                    return TextMsg(toUserName, fromUserName,
                                   "出现错误，请联系管理员").structReply()
            finally:
                try:
                    reply_content = "已切换{} \n等待时间: 5-30 秒 \n单价: {} 元 \n请勿重复提交 \n请发送 15 位 imei 或 12 位序列号查询".format(
                        event_list[eventKey]["name"],
                        event_list[eventKey]["count"])
                except KeyError as exc:
                    if exc.args[0] == "count":
                        if eventKey == "RECHARGE":
                            return eventKey, openid
                        else:
                            TextMsgObj = TextMsg(toUserName, fromUserName,
                                                 "该服务还没准备好哦，请稍后")
                        # return "is_render", openid
                else:
                    TextMsgObj = TextMsg(toUserName, fromUserName,
                                         reply_content)

                return TextMsgObj.structReply()


class TextMsg:
    def __init__(self, toUser, fromUser, recvMsg):
        self._toUser = toUser
        self._fromUser = fromUser
        self._recvMsg = recvMsg
        self._nowTime = int(time.time())

    def structReply(self):
        content = self._recvMsg
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{3}]]></Content>
                </xml>
                """.format(self._fromUser, self._toUser, self._nowTime,
                           content)  #前面两个参数的顺序需要特别注意
        #    "感谢您的关注，公众号尚处于开发过程中，请稍后查询，谢谢")  #前面两个参数的顺序需要特别注意

        return text


class ImageMsg:
    def __init__(self, toUser, fromUser, mediaId):
        self._toUser = toUser
        self._fromUser = fromUser
        self._rediaId = mediaId
        self._nowTime = int(time.time())
        self._mediaId = mediaId

    def structReply(self):
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{3}]]></MediaId>
                </Image>
                </xml>
                """.format(self._fromUser, self._toUser, self._nowTime,
                           self._mediaId)  #前面两个参数的顺序需要特别注意

        return text


if __name__ == "__main__":
    # os.chdir(
    #     os.path.dirname(
    #         "C:/UsersShadowMimosa/Documents/GitRepository/Workoo/now/wx_service/"
    #     ))
    body = """
            <xml>       
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[FromUser]]></FromUserName>
                <CreateTime>123456789</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[CLICK]]></Event>
                <EventKey><![CDATA[EVENTKEY]]></EventKey>
            </xml>
            """
    Analysis().prase(smart_str(body))