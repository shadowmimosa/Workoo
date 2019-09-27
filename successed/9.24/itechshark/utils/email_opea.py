import poplib
from email.parser import Parser
from email.utils import parseaddr
from email.header import decode_header


class ReadEmail(object):
    def __init__(self, accout, password, pop_host="pop.qq.com"):
        self.accout = accout
        self.password = password
        self.pop_host = pop_host

        self.body_contents = []

        self.init_pop_server()

    def init_pop_server(self):
        poplib._MAXLINE = 20480

        pop_server = poplib.POP3(self.pop_host)
        pop_server.user(self.accout)
        pop_server.pass_(self.password)

        self.popServer = pop_server

    def del_email(self):
        self.popServer.dele()

    def decode_msg_header(self, header):
        """
        解码头文件
        :param header: 需解码的内容
        :return:
        """
        value, charset = decode_header(header)[0]
        if charset:
            value = value.decode(charset)
        return value

    def guess_charset(self, content):
        charset = content.get_charset()
        if charset is None:
            content_type = content.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def decode_body(self, content):
        """
        解码内容
        :param content: 邮件某部分
        """
        contentType = content.get_content_type()  # 判断邮件内容的类型,text/html
        textContent = ""
        if contentType == 'text/plain' or contentType == 'text/html':
            content = content.get_payload(decode=True)
            charset = self.guess_charset(content)
            if charset:
                textContent = content.decode(charset)
        return textContent

    def get_email_object(self, msg_index=1):
        resp, mails, octets = self.popServer.list()
        index = len(mails)

        while index == 0:
            resp, mails, octets = self.popServer.list()
            index = len(mails)

        # 获取第msgIndex封邮件的信息
        response, msg_lines, octets = self.popServer.retr(index)
        # msgLines中为该邮件的每行数据,先将内容连接成字符串，再转化为email.message.Message对象
        msg_str = b"\r\n".join(msg_lines).decode("utf8", "ignore")
        self.messageObject = Parser().parsestr(msg_str)
        self.popServer.dele(index)
        self.popServer.quit()

    def get_email_sender(self):

        sender_content = self.messageObject["From"]
        # parseaddr()函数返回的是一个元组(realname, emailAddress)
        sender_name, sender_address = parseaddr(sender_content)
        # 将加密的名称进行解码
        return self.decode_msg_header(sender_name)

    def get_email_content(self, msg):
        if msg.is_multipart():
            msg_parts = msg.get_payload()
            for msg_part in msg_parts:
                self.get_email_content(msg_part)
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = self.guess_charset(msg)
                if charset:
                    self.body_contents.append(content.decode(charset))
            else:
                # 不是文本,作为附件处理:
                pass

    def get_email_body(self):

        return self.body_contents

    def run(self):
        self.get_email_object()
        if self.get_email_sender() == "iTechshark":
            self.get_email_content(self.messageObject)
            return self.body_contents


if __name__ == "__main__":
    ReadEmail(accout="", password="").main()
