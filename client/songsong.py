
#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
# 导入ttk
from tkinter import ttk
# 导入filedialog
from tkinter import filedialog
import pandas as pd
import time
import datetime
from tkinter import messagebox as msgbox


class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()

    def initWidgets(self):
        # 创建按钮，并为之绑定事件处理函数
        ttk.Button(self.master, text='Open EXCEL',
                   command=self.open_file  # 绑定open_file方法
                   ).pack(side=BOTTOM, ipadx=150, ipady=100)

    def open_file(self):
        # 调用askopenfile方法获取单个打开的文件
        file_path = filedialog.askopenfilename(title='打开单个文件',
                                               filetypes=[("office10-19", "*.xlsx"), ('office03-07', '*.xls')],
                                               # 只处理的文件类型
                                               initialdir='./')  # 初始目录
        # print(file_path)
        self.exec_file(file_path)
        msgbox.showinfo(title='提示', message='处理完成')

    def exec_file(self, file_name):
        f = pd.read_excel(file_name, header=0)
        df = pd.DataFrame(f)
        # print(df)
        new_name = datetime.datetime.now().strftime('%Y-%m-%d') + ".xlsx"
        data = []

        for row in df.itertuples(name="RowData"):
            order_time = row[1]  # 下单时间
            receive_time = row[4]  # 妥投时间
            aging = row[13]  # 时效
            flag = row[14]  # 是否超时
            t4 = datetime.datetime.strptime(receive_time, "%Y-%m-%d %H:%M:%S")
            t5 = datetime.datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
            result = t4.__sub__(t5)
            if result.seconds > aging * 60 * 60:
                data.append('是')
            else:
                data.append('否')

            # 判断每一条记录'是否超时'
        f['是否超时'] = data
        # print(f)
        f.to_excel(file_name, '明细表', index=False, header=True)


root = Tk()
root.title("小枀康葆")
App(root)
root.mainloop()