import tkinter as tk
from tkinter import ttk

from spider_amazon import Amazon


def make_it():
    mode = var1.get()
    proxy = var2.get()
    interval = var3.get()

    spider.proxy=proxy
    spider.sleep_time=interval

    if mode == 0:
        Text1.insert('insert', 'Error: 请选择 Cookie 获取方式\n')
        Text1.see(tk.END)
    elif mode == 1:
        spider.run()
        pass
    elif mode == 2:
        pass
    text = Text1.get('0.0', 'end')
    print(text)
    pass


spider = Amazon()
windows = tk.Tk()
windows.geometry('600x325')
windows.resizable(0, 0)

windows.title('Amazon 采集')

var1 = tk.IntVar()
var1.set(0)
var2 = tk.IntVar()
var2.set(0)

r1 = tk.Radiobutton(windows, text='自动获取 Cookies', variable=var1, value=1)

r1.place(height=20, width=120, x=15, y=15)
# r1.grid(row=0, column=0, padx=5, pady=5)
r2 = tk.Radiobutton(windows, text='手动导入 Cookie', variable=var1, value=2)
r2.place(height=20, width=120, x=150, y=15)
# r2.grid(row=0, column=1, padx=5, pady=5)

r3 = tk.Radiobutton(windows, text='使用代理', variable=var2, value=1)
r3.place(height=20, width=120, x=285, y=15)
# r3.grid(row=0, column=2, padx=5, pady=5)

Label1 = tk.Label(windows, text='请求间隔(秒): ')
# Label1.grid(row=1, column=0, padx=30, pady=5, sticky='W')
Label1.place(height=20, width=120, x=15, y=50)

var3 = tk.IntVar()
c1 = ttk.Combobox(textvariable=var3)
c1['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
# numberChosen.grid(column=1, row=1)
c1.current(0)
c1.place(height=20, width=120, x=150, y=50)
# c1.grid(row=1, column=1, padx=0, pady=0, sticky='W')

Button1 = tk.Button(windows, text='采集', command=make_it)
Button1.place(height=40, width=90, x=420, y=25)
# Button1.grid(row=1, column=2, padx=10, pady=10)  # , rowspan=2, columnspan=2

Text1 = tk.Text(windows)
Text1.insert('insert', '初始化程序...\n')
Text1.place(height=120, width=570, x=15, y=90)
# Text1.grid(row=3, column=1)

Label1 = tk.Label(
    windows,
    justify='left',
    text=
    '采集程序使用说明: \n采集链接放在程序目录下 links.txt 中, 每行放一个链接; 使用熊猫代理, 链接放在程序目录下 proxy.txt 中\n'
)
Label1.place(height=60, width=570, x=15, y=225)

Label2 = tk.Label(
    windows,
    justify='left',
    text=
    '选项一: 后台静默打开网页自动化切换地区获取 Cookie, 影响因素较多, 可能会出错\n选项二: 手动导入 Cookie, 略过自动获取, Cookie 失效时间未知'
)
Label2.place(height=60, width=450, x=20, y=260)

windows.mainloop()