import json
import urllib3
import requests

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.session()
session.verify = False
resp = session.post('https://sy.kuakuavideo.com/kuaishou',
                    json={
                        "sourceURL":
                        # "https://www.ixigua.com/i6748968448862192141/",
                        "https://www.ixigua.com/i6772442821258379780/",
                        "e": "",
                        "r": "",
                        "ticket": "",
                        "randstr": ""
                    })

data = json.loads(resp.text)
print()
'http://v29-tt.ixigua.com/77099176d07d6feeba7b266c7fd94f60/5e4a0d9d/video/tos/cn/tos-cn-v-0000/5e4e630d36a34afe9fa08afdcd2040c6/?a=1768&br=39210&bt=19605&cr=0&cs=0&dr=0&ds=4&er=&l=202002171050080100140470131011279F&lr=&qs=13&rc=andzeDtzNXg7cTMzPDczM0ApOHQ0djxkdXF4ZTMzZjM1eWcybi5wNl5va3JfLS1gLS9zc2RxbXI1bS9yNWstLTYxLS06Yw%3D%3D&vl=&vr='
'http://v29-tt.ixigua.com/77099176d07d6feeba7b266c7fd94f60/5e4a0d9d/video/tos/cn/tos-cn-v-0000/5e4e630d36a34afe9fa08afdcd2040c6/?a=1768&br=39210&bt=19605&cr=0&cs=0&dr=0&ds=4&er=&l=202002171050080100140470131011279F&lr=&qs=13&rc=andzeDtzNXg7cTMzPDczM0ApOHQ0djxkdXF4ZTMzZjM1eWcybi5wNl5va3JfLS1gLS9zc2RxbXI1bS9yNWstLTYxLS06Yw%3D%3D&vl=&vr='


http://v6-tt.ixigua.com/0c141853c4edf3f469400b565368c2d8/5e4a2264/video/tos/cn/tos-cn-v-0000/b72e9164eca34937b98a2861f19c40b2/?a=1768&br=21014&bt=10507&cr=0&cs=0&dr=0&ds=4&er=&l=202002171219100100100631490C00C6F3&lr=&qs=13&rc=M2Q2aW14bWw5bDMzZDczM0ApbmdoaGo4eHN2ZTMzZTM1eWdoYWJiZDJybXBfLS1fLS9zcy1eMGNncmdmM2YtLV4xLS06Yw%3D%3D&vl=&vr=
http://v6-tt.ixigua.com/3e9086890e61b9e97135ae812ee069e1/5e4a2292/video/tos/cn/tos-cn-v-0000/b72e9164eca34937b98a2861f19c40b2/?a=1768&br=21014&bt=10507&cr=0&cs=0&dr=0&ds=4&er=&l=202002171219560100140400860D011564&lr=&qs=13&rc=M2Q2aW14bWw5bDMzZDczM0ApbmdoaGo4eHN2ZTMzZTM1eWdoYWJiZDJybXBfLS1fLS9zcy1eMGNncmdmM2YtLV4xLS06Yw%3D%3D&vl=&vr=