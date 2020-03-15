import tkinter as tk


def make_it():
    text = Text.get('0.0','end')
    Text1
    print(text)
    pass


windows = tk.Tk()
windows.geometry('600x325')
windows.resizable(0, 0)
windows.title('无水印解析 BY：ShadowMimosa')

Text1 = tk.Text(windows)
Text1.place(height=90, width=465, x=25, y=25)

Button1 = tk.Button(windows, text='解析', command=make_it)
Button1.place(height=25, width=60, x=515, y=52.5)

Label1 = tk.Label(windows,
                          text='video简介',
                          justify='left',
                          wraplength=508,
                          anchor='n')
Label1.place(height=25, width=550, x=25, y=140)

# Label2 = tk.Label(windows,text='video简介\nfghjk\n')
# Label2.place(height=25, width=508, x=42, y=158)

Text = tk.Text(windows)
Text.place(height=90, width=550, x=25, y=210)

windows.mainloop()
