import asyncio
import random, time

from pyppeteer import launch
from retrying import retry


class UnderWear(object):
    def __init__(self, page):
        self.shoplist = [
            "都市丽人官方旗舰店", "浪莎官方旗舰店", "安莉芳官方旗舰店", "奥丽侬官方旗舰店", "黛安芬官方旗舰店"
        ]
        self.shop_url = [
            "https://dushiliren.tmall.com/search.htm?spm=a1z10.3-b-s.0.0.15817191N5vpnX&search=y",
            "https://embryform.tmall.com/category-1325352900.htm?spm=a1z10.1-b-s.w12012752-16996982169.7.10f03608JRsXXN&search=y&parentCatId=951852586&parentCatName=%C8%AB%B2%BF%B1%A6%B1%B4&catName=%CE%C4%D0%D8%D7%A8%C7%F8&scene=taobao_shop#bd"
        ]
        self.page = page
        self.run()

    async def main(self, url):
        new_page = await self.page.goto(url)
        pass

    def run(self):
        for value in self.shop_url:
            self.main(value)


async def main(username, pwd, url):
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({
        'headless':
        False,
        'dumpio':
        True,
        'args': [
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
        ],
    })
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    )
    await page.goto(url)

    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)

    await page.type('.J_UserName', username,
                    {'delay': input_time_random() - 50})
    await page.type('#J_StandardPwd input', pwd,
                    {'delay': input_time_random()})

    time.sleep(2)

    slider = await page.Jeval('#nocaptcha', 'node => node.style')
    if slider:
        print('当前页面出现滑块')
        flag, page = await mouse_slide(page=page)
        if flag:
            await page.keyboard.press('Enter')
            print("print enter", flag, page)
            await page.evaluate(
                '''document.getElementById("J_SubmitStatic").click()''')
            time.sleep(2)
            cookies = await get_cookie(page)

        else:
            print("print enter", flag, page)
    else:
        print("")
        await page.keyboard.press('Enter')
        print("print enter")
        # await page.waitFor(5)
        # await page.evaluate(
        #     '''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(20)
        await page.waitForNavigation()

        try:
            error = await page.Jeval('.error', 'node => node.textContent')
            print("error_2:", error)
        except Exception as e:
            error = None
            print('发生错误：', e)
        finally:
            if error:
                print('确保账户安全重新入输入')
                # 程序退出。
                loop.close()
            else:
                print(page.url)
                cookies = await get_cookie(page)

    return cookies, page


js1 = '''() =>{
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }'''

js2 = '''() => {
            alert (
            window.navigator.webdriver
            )
        }'''

js3 = '''() => {
            window.navigator.chrome = {
            runtime: {},
            // etc.
            };
        }'''

js4 = '''() =>{
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        }'''

js5 = '''() =>{
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5,6],
            });
        }'''


# 获取登录后cookie
async def get_cookie(page):
    #res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


def input_time_random():
    return random.randint(100, 151)


def retry_if_result_none(result):
    return result is None


@retry(
    retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        print('开始验证...')
        await page.hover('#nc_1_n1z')
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        slider_again = await page.Jeval('.nc-lang-cnt',
                                        'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page


if __name__ == '__main__':
    username = 'tb4986521_2013'  # 账号
    pwd = 'taobao6521'  #密码
    url = 'https://login.taobao.com/member/login.jhtml?style=mini&from=b2b&full_redirect=true'
    loop = asyncio.get_event_loop()
    result, page = loop.run_until_complete(main(username, pwd, url))
    print('登录后cookies:', result)
    UnderWear(page)
