import pythoncom, win32con
import PyHook3 as pyHook
import win32api, threading

preKey = ''
timer = False  # 定时器
isQuiet = False  # 是否暂停程序功能，为true时暂停程序功能
isTimer = False  # 是否已存在定时器，为true时存在定时器


def func_timer():
    global preKey, timer, isTimer
    preKey = ''
    timer.cancel()
    isTimer = False


def onKeyboardEvent(event):
    global timer, isQuiet, isTimer, LmenuState, shiftState
    LmenuState = win32api.GetKeyState(18)
    shiftState = win32api.GetKeyState(16)
    if isTimer:
        timer.cancel()
    global preKey, currentKey
    currentKey = str(event.Key)
    # 如果当前按键为alt/lshift/rshift,将其值存储到prekey，本次按键监听结束，程序进入下一次按键监听。
    if currentKey == 'Lmenu' or currentKey == 'Lshift' or currentKey == 'Rshift':
        preKey = str(event.Key)
        return True
    # 如果当前按键为tab,则进入prekey判断
    if currentKey == 'Tab':
        # (win32api.GetKeyState(20) == 1)表示大写键被锁定
        # prekey为以下几个值，说明用户操作的是原有的快捷键，不做键盘消息处理，本次监听结束，进入下一次按键监听
        # 存在bug：为了使alt/shift加tab能连续使用，未清除记录的alt/shift键状态,此时立即按tab键，不会进入快捷方式
        # 修复方案，需获取alt的按键状态，win32ap.GetKeyState获取的是使用情况，比如初次win32ap.GetKeyState(16)为1，
        # 按一次shift后，win32ap.GetKeyState(16)=0，再按一次shift win32ap.GetKeyState(16)又变为1
        if preKey == 'Lmenu' or preKey == 'Lshift' or preKey == 'Rshift':
            # 状态为-128或-127,则表明该键处于按下状态
            # （若当前状态为0，则长按时，获取到的状态值为-127；若当前状态为0，则长按时，获取到的状态值为-128）
            if LmenuState == -128 or LmenuState == -127 or shiftState == -128 or shiftState == -127:
                return True
            else:
                preKey = 'Tab'
                return False
        #
        if preKey != 'Tab':
            preKey = str(event.Key)
            timer = threading.Timer(1, func_timer)
            timer.start()
            isTimer = True
            # 如果程序功能不为暂停，则阻止程序往下执行
            if not isQuiet:
                return False
    if preKey == 'Tab':
        if currentKey == 'Q':  # 按下Q后暂停快捷键功能
            isQuiet = not isQuiet
            preKey = ''
            return False
        if not isQuiet:
            preKey = ''
            if currentKey == 'M':
                win32api.keybd_event(9, 0, 0, 0)
                win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
                return False
            # 逗号
            if currentKey == 'Oem_Comma':
                win32api.keybd_event(35, 0, 0, 0)
                win32api.keybd_event(event.KeyID, 0, 0, 0)
                win32api.keybd_event(event.KeyID, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(13, 0, 0, 0)
                # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
                return False
                # win32api.keybd_event(event.KeyID, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)  # 按下键位
                # win32api.keybd_event(event.KeyID, 0, win32con.KEYEVENTF_KEYUP, 0)  # 松开键位
            # 分号
            if currentKey == 'Oem_1':
                win32api.keybd_event(35, 0, 0, 0)
                win32api.keybd_event(event.KeyID, 0, 0, 0)
                win32api.keybd_event(event.KeyID, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(13, 0, 0, 0)
                return False
            # Left
            if currentKey == 'J':
                win32api.keybd_event(37, 0, 0, 0)
                return False
            # Up
            if currentKey == 'I':
                win32api.keybd_event(38, 0, 0, 0)
                return False
            # Right
            if currentKey == 'L':
                win32api.keybd_event(39, 0, 0, 0)
                return False
            # Down
            if currentKey == 'K':
                win32api.keybd_event(40, 0, 0, 0)
                return False
            # =
            if currentKey == 'O':
                win32api.keybd_event(32, 0, 0, 0)  # 空格
                win32api.keybd_event(187, 0, 0, 0)
                win32api.keybd_event(187, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(32, 0, 0, 0)  # 空格
                return False
            # +
            if currentKey == 'P':  # ;
                win32api.keybd_event(32, 0, 0, 0)  # 空格
                win32api.keybd_event(16, 0, 0, 0)  # shift
                win32api.keybd_event(187, 0, 0, 0)  # "=+"
                win32api.keybd_event(187, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(32, 0, 0, 0)  # 空格
                return False
            # :
            if currentKey == 'U':
                win32api.keybd_event(35, 0, 0, 0)  # 按下End
                win32api.keybd_event(16, 0, 0, 0)  # 按下Shift
                win32api.keybd_event(186, 0, 0, 0)  # 按下“;:”
                win32api.keybd_event(186, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(13, 0, 0, 0)  # 按下“Enter”
                return False
            # {}
            if currentKey == 'Oem_4':  # [
                win32api.keybd_event(35, 0, 0, 0)  # 按下End
                win32api.keybd_event(32, 0, 0, 0)  # 按下Space
                win32api.keybd_event(16, 0, 0, 0)  # 按下Shift
                win32api.keybd_event(219, 0, 0, 0)  # 按下“[{”
                win32api.keybd_event(219, 0, win32con.KEYEVENTF_KEYUP, 0)  # 松开shift
                win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)  # 松开“[{”
                win32api.keybd_event(16, 0, 0, 0)
                win32api.keybd_event(221, 0, 0, 0)
                win32api.keybd_event(221, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(37, 0, 0, 0)
                win32api.keybd_event(13, 0, 0, 0)
                return False
            # 打开txt
            if currentKey == 'T':
                win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', win32con.SW_SHOW)
                return False
            # # 打开word
            # if currentKey == 'W':
            #     win32api.ShellExecute(0, 'open', 'word.exe', '', '', win32con.SW_SHOW)
            #     return False
            # 以默认浏览器打开百度
            if currentKey == 'G':
                win32api.ShellExecute(0, 'open', 'https://baidu.com', '', '', win32con.SW_SHOW)
                return False
            # 以默认浏览器打开有道翻译
            if currentKey == 'Y':
                win32api.ShellExecute(0, 'open', 'http://fanyi.youdao.com/', '', '', win32con.SW_SHOW)
                return False
        if currentKey == 'F12':  # 按下F12后终止
            win32api.PostQuitMessage()
            return False
    if currentKey != 'Tab':
        preKey = ''
    return True


def openEXE(name, bool):
    win32api.ShellExecute(0, 'open', name, '', '', bool)


if __name__ == "__main__":
    # 创建hook句柄
    hm = pyHook.HookManager()

    # 监控键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()

    # 循环获取消息
    pythoncom.PumpMessages(10000)