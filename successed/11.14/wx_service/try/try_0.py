from PIL import Image
import io
import json
import time
from wechat.utils.request import Query

resp = Query().run(
    path=
    "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQFy7jwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAybU1tc3Bsb3BlWmwxdE1DVmh0Y0EAAgRwWVJdAwQAjScA",
    sign=1)
# print(resp)
# iost = resp
iost = io.BytesIO(resp)
# iost = io.StringIO(resp)
init_pic = Image.open("C:/Users/ShadowMimosa/Desktop/init.jpg")
# init_pic = Image.open("C:/Users/ShadowMimosa/Desktop/1565681901897.jpg")
# qrcode = Image.open("C:/Users/ShadowMimosa/Desktop/qrcode.png")
# with open("C:/Users/ShadowMimosa/Desktop/qrcode.png", "rb") as fn:
#     qr = fn.read()
# qrcode = Image.frombytes("RGBA", (100, 100), resp, 'raw')
qrcode = Image.open(iost)
size = qrcode.size
qrcode = qrcode.resize((800, 800))
print(size)
# qrcode = Image.fromstring("RBG", (80, 80), iost)
# Image.open()

# init_pic.paste(qrcode, (172, 454))
init_pic.paste(qrcode, (460, 1600))
byte_io = io.BytesIO()
init_pic.save(byte_io, 'jpeg')
byte_io.seek(0)
init_pic.show()
init_pic.save("C:/Users/ShadowMimosa/Desktop/fina_0.jpg")
files = {
    'media': ('qrcode.jpg', byte_io),
}
resp = Query().run(
    path=
    "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=24_BIVT2rJbJP-b-xloRTVCV0Y0vmRy4pwRUJ_yrmzdeBHhPBqlYJjnjPep7ktBN5AK70w3E6g1pxkbabhxwv79PJ58hqsjFJCFMzKHi45wCu_Y0_MQ-HOJ5dpHQDPSA7BsWw03BHCUSIP1p7krQVTjACAZEC&type=image",
    files=files)

resp = Query().run(
    path=
    "https://api.weixin.qq.com/cgi-bin/media/get?access_token=24_BIVT2rJbJP-b-xloRTVCV0Y0vmRy4pwRUJ_yrmzdeBHhPBqlYJjnjPep7ktBN5AK70w3E6g1pxkbabhxwv79PJ58hqsjFJCFMzKHi45wCu_Y0_MQ-HOJ5dpHQDPSA7BsWw03BHCUSIP1p7krQVTjACAZEC&media_id={}"
    .format(json.loads(resp)["media_id"]))
print(resp)
print(init_pic)
init_pic.show()

# from MyQR import myqr

# myqr.Image()