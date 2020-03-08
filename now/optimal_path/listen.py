import threading
import socket
import time
import json

encoding = 'utf-8'
BUFSIZE = 1024


# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        #while True:
        data = self.client.recv(BUFSIZE)
        if (data):
            string = bytes.decode(data, encoding)
            print("from client::", string, "")
            # time.sleep(10)
            # self.client.send(bytes("return from server::" + string, encoding))
            msg = "HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n" + string
            # self.client.send(msg.encode(encoding))
            msg = 'HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\n\r\n' + json.dumps(
                {'id': 'test'})
            self.client.send(msg.encode(encoding))
            self.client.close()
            # self.client.send(''.encode(encoding))

        # print("close:", self.client.getpeername())

    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = bytes.decode(rec, encoding)
            if len(string) > 2:
                string = string[0:-2]
            else:
                string = ' '
        else:
            string = False
        return string


# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(5)

    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            print("accept a connect...")
            Reader(client).start()
            cltadd = cltadd
            print("accept a connect(new reader..)")


lst = Listener(8888)  # create a listen thread
lst.start()  # then start

# Now, you can use telnet to test it, the command is "telnet 127.0.0.1 9011"
# You also can use web broswer to test, input the address of "http://127.0.0.1:9011" and press Enter button
# Enjoy it....