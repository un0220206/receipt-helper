import tkinter
from tkinter import ttk
import os
import time
import re
import ctypes 
import requests #需要安裝
from bs4 import BeautifulSoup #需要安裝
import matplotlib.pyplot as plt #需要安裝
import numpy as np #需要安裝
def center_window(root, width, height):  
    screenwidth = root.winfo_screenwidth()  
    screenheight = root.winfo_screenheight()  
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)
def file(name):
    allFile = os.listdir("./"); file = []
    for f in allFile:
        if f.find(name) >= 0: file.append(f)
    return file
def checkAward(ownReceipt, receipt, canvas, layout):
    receipt1 = [receipt['first'], receipt['second'], receipt['third']]
    receipt2 = [receipt['add1'], receipt['add2'], receipt['add3']]
    amount = [0, '']
    if ownReceipt == receipt['special']:
        canvas.create_text(5, layout[0], text = '恭喜中特別獎 10,000,000元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
        amount = [10000000, 'special']
    elif ownReceipt == receipt['special1']:
        canvas.create_text(5, layout[0], text = '恭喜中特獎 2,000,000元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
        amount = [2000000, 'particular']
    for firstReceipt in receipt1:
        if ownReceipt == firstReceipt:
            canvas.create_text(5, layout[0], text = '恭喜中頭獎 200,000元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
            amount = [200000, 'first']
        elif ownReceipt[-7:] == firstReceipt[-7:]:
            canvas.create_text(5, layout[0], text = '恭喜中二獎 40,000元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
            amount = [40000, 'second']
        elif ownReceipt[-6:] == firstReceipt[-6:]:
            canvas.create_text(5, layout[0], text = '恭喜中三獎 10,000元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
            amount = [10000, 'third']
        elif ownReceipt[-5:] == firstReceipt[-5:]:
            canvas.create_text(5, layout[0], text = '恭喜中四獎 4,000元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
            amount = [4000, 'fourth']
        elif ownReceipt[-4:] == firstReceipt[-4:]:
            canvas.create_text(5, layout[0], text = '恭喜中五獎 1,000元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
            amount = [1000, 'fifth']
        elif ownReceipt[-3:] == firstReceipt[-3:]:
            canvas.create_text(5, layout[0], text = '恭喜中六獎 200元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
            amount = [200, 'sixth']
    for addReceipt in receipt2:
        if ownReceipt[-3:] == addReceipt[-3:]:
            canvas.create_text(5, layout[0], text = '恭喜中增開六獎 200元：' + ownReceipt, font = 30, fill = 'darkred', anchor = 'nw')
            amount = [200, 'addsixth']
    return amount
def compare(award):
    amount = award
    if award >= 4000:
        amount = award - (award * 0.004) - (award * 0.2)
    elif award == 1000:
        amount = award - (award * 0.004)
    return amount
def checkBigThenZero(award, receipt, fileName):
    fileType = 'a' if os.path.isfile('{0}中獎發票.txt'.format(fileName)) else 'x'
    if award > 0:
        with open('{0}中獎發票.txt'.format(fileName), fileType) as file1:
            file1.writelines('{0}: {1}元獎金\n'.format(receipt, format(award, ',')))
        return True
    return False
def compareReceipt(receiptfile, receipt, canvas, layout, fileName):
    sum = 0; tax = 0
    award = checkAward(receipt, receiptfile, canvas, layout)
    if checkBigThenZero(award[0], receipt, fileName): sum = award[0]; tax = compare(award[0])
    return [sum, tax, award[1]] if len(award) == 2 else [sum, tax]
def checkReceipt(receipt):
    return False if len(receipt) != 8 or not(receipt.isdigit()) else True
def getReceipt(fileName):
    with open('{0}.txt'.format(fileName)) as file1:
        special = file1.readline().replace('\n', '')
        special1 = file1.readline().replace('\n', '')
        first = file1.readline().replace('\n', '')
        second = file1.readline().replace('\n', '')
        third = file1.readline().replace('\n', '')
        add1 = file1.readline().replace('\n', '')
        add2 = file1.readline().replace('\n', '')
        add3 = file1.readline().replace('\n', '')
        receipt = dict([('special', special), ('special1', special1), ('first', first),
                     ('second', second), ('third', third), ('add1', add1), 
                     ('add2', add2), ('add3', add3)])
    return receipt
def checkAmount(fileName, sum, tax):
    p_sum = 0; p_tax = 0
    if os.path.isfile(fileName + '金額.txt'):
        fileType = 'w'
        with open(fileName + '金額.txt') as file1:
            p_sum = file1.readline().replace(',', '').replace('\n', '')
            p_tax = file1.readline().replace(',', '').replace('\n', '')
    else:
        fileType = 'x'
    with open(fileName + '金額.txt', fileType) as file1:
        file1.writelines('{0}\n'.format(format(int(sum) + int(p_sum), ',')))
        file1.writelines('{0}\n'.format(format(int(tax) + int(p_tax), ',')))
def checkAllAmount(fileDate):
    if os.path.isfile('金額.txt'):
        with open('金額.txt') as file1:
            n_sum = file1.readline().replace(',', '').replace('\n', '')
            n_tax = file1.readline().replace(',', '').replace('\n', '')
        checkAmount(fileDate, n_sum, n_tax)
        os.remove('金額.txt')
        return [format(int(n_sum), ','), format(int(n_tax), ',')]
    else:
        return '很可惜您並沒有中任何的獎項'
def winReceiptPOrNot(win, notWin, fileName, whereAward):
    size = []; i = 2; award = {'special':2, 'particular':3, 'first':4, 'second':5, 'third':6, 'fourth':7, 'fifth':8, 'sixth':9, 'addsixth':10}
    if os.path.isfile(fileName + '中獎機率.txt'):
        fileType = 'w'
        with open(fileName + '中獎機率.txt') as file:
            for line in file.readlines(): size.append(int(line))
    else:
        fileType = 'x'; size= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    with open(fileName + '中獎機率.txt', fileType) as file:
        file.writelines(str(size[0] + win) + '\n')
        file.writelines(str(size[1] + notWin) + '\n')
        while(len(size) > i):
            if award.get(whereAward) == i:
                file.writelines(str(size[i] + 1) + '\n')
            else:
                file.writelines(str(size[i] + 0) + '\n')
            i += 1
def reciptLotteryAlready():
    def goBack():
        for fileName in allAmount:
            if allAmount.get(fileName)[0] > 0:
                ctypes.windll.user32.MessageBoxW(0, '恭喜您總共中了' + format(allAmount.get(fileName)[0], ',') + 
                    '元\n扣稅後，總金額為' + format(allAmount.get(fileName)[1], ',') + '元', '{0}中獎金額'.format(fileName), 0)
            else:
                ctypes.windll.user32.MessageBoxW(0, '很可惜您並沒有中任何的獎項', '{0}中獎金額'.format(fileName), 0)
        reciptAlreadyList.destroy()
    layout = [0, 1, 500]; sum = 0; fileNameList = file('未開獎'); allAmount = dict()
    reciptAlreadyList= tkinter.Tk()
    reciptAlreadyList.title('對之前已輸入發票')  
    center_window(reciptAlreadyList, 400, 400)
    reciptAlreadyList.resizable(width = False, height = False)
    reciptAlreadyList.after(1, lambda: reciptAlreadyList.focus_force())
    button1 = tkinter.Button(reciptAlreadyList, text = "返回", font = 30, command = goBack)
    button1.place(x = 345, y = 365)
    if len(fileNameList) == 0:
        label1 = tkinter.Label(reciptAlreadyList, text = '您未輸入未開獎發票', font = 30)
        label1.place(x = 5, y = 5)
    else:
        canvas = tkinter.Canvas(reciptAlreadyList, width = 400, height = 365, scrollregion = (0, 0, 0, 500))
        vbar = tkinter.Scrollbar(canvas,orient = 'vertical')
        vbar.place(x = 377, y = 0, width = 20, height = 360)
        vbar.config(command = canvas.yview)
        canvas.config(yscrollcommand = vbar.set)
        canvas.place(x = 0, y = 0)
        for fileName in fileNameList:
            fileDate = fileName.replace('未開獎', '')
            if os.path.isfile(fileDate):
                fileDate = fileDate.replace('.txt', ''); layout[0] += 10
                canvas.create_text(5, layout[0], text = fileDate + '：', font = 30, anchor = 'nw')
                layout[0] += 25
                with open(fileName) as file1:
                    receiptfile = getReceipt(fileDate)
                    sum = 0; tax = 0
                    for line in file1.readlines():
                        receipt = line.replace('\n', '')
                        amount = compareReceipt(receiptfile, receipt, canvas, layout, fileDate)
                        if int(amount[0]) == 0:
                            canvas.create_text(5, layout[0], text = '沒有中獎: ' + receipt, font = 30, fill = 'darkblue', anchor = 'nw')
                            winReceiptPOrNot(0, 1, fileDate, '')
                            winReceiptPOrNot(0, 1, '總', '')
                        else:
                            sum += int(amount[0]); tax += int(amount[1])
                            winReceiptPOrNot(1, 0, fileDate, amount[2])
                            winReceiptPOrNot(1, 0, '總', amount[2])
                        if layout[1] % 20 == 0: layout[2] += 500; canvas.config(scrollregion = (0, 0, 0, layout[2]))
                        layout[0] += 25; layout[1] += 1
                if sum > 0:
                    checkAmount(fileDate, sum, tax)
                os.remove(fileName); allAmount['{0}'.format(fileDate)] = [sum, tax]
            else:
                layout[0] += 10
                canvas.create_text(5, layout[0], text = fileDate.replace('.txt', '') + '未開獎', font = 30, fill = 'darkgreen', anchor = 'nw')
                layout[0] += 25
            reciptAlreadyList.protocol('WM_DELETE_WINDOW', goBack)
    reciptAlreadyList.mainloop()
def reciptLottery():
    def confirm(entry, canvas, layout, receiptfile, fileDate):
        firstOrNot[1] = False; firstOrNot[0] = True
        if len(entry.get()) > 0:
            if checkReceipt(entry.get()):
                amount = []
                amount = compareReceipt(receiptfile, entry.get(), canvas, layout, fileDate)
                if int(amount[0]) == 0:
                    winReceiptPOrNot(0, 1, fileDate, '')
                    winReceiptPOrNot(0, 1, '總', '')
                    canvas.create_text(5, layout[0], text = '沒有中獎: ' + entry.get(), font = 30, fill = 'darkblue', anchor = 'nw')
                else:
                    winReceiptPOrNot(1, 0, fileDate, amount[2])
                    winReceiptPOrNot(1, 0, '總', amount[2])
                    sum = amount[0]; tax = amount[1]
                    checkAmount('', sum, tax)
            else:
                canvas.create_text(5, layout[0], text = '輸入錯誤發票號碼', font = 30, anchor = 'nw')            
            if layout[1] % 20 == 0: layout[2] += 500; canvas.config(scrollregion = (0, 0, 0, layout[2]))
            layout[1] += 1; layout[0] += 25; entry.delete(0, 'end')
    def confirmDate(event):
        layout = [10, 1, 500]
        fileDate = combox.get()
        receiptfile = getReceipt(fileDate)
        label2 = tkinter.Label(reciptList, text = '請輸入您的發票號碼：', font = 30)
        label2.place(x = 5, y = 80)
        entry = tkinter.Entry(reciptList, font = 30)
        entry.place(x = 5, y = 110)
        entry.focus()
        entry.bind('<Return>', lambda e: confirm(entry, canvas, layout, receiptfile, fileDate))
        canvas = tkinter.Canvas(reciptList, width = 400, height = 220, scrollregion = (0, 0, 0, 500))
        vbar = tkinter.Scrollbar(canvas, orient = 'vertical')
        vbar.place(x = 370, y = 0, width = 20, height = 220)
        vbar.config(command = canvas.yview)
        canvas.config(yscrollcommand = vbar.set)
        canvas.place(x = 0, y = 140)
        if firstOrNot[0]:
            for date in comboxOption:
                if fileDate != date:
                    amount = checkAllAmount(date)
                    if isinstance(amount, list):
                        ctypes.windll.user32.MessageBoxW(0, '恭喜您總共中了' + amount[0] + 
                            '元\n扣稅後，總金額為' + amount[1] + '元', '{0}中獎金額'.format(date), 0)
                    else:
                        ctypes.windll.user32.MessageBoxW(0, amount, '{0}中獎金額'.format(date), 0)
                    firstOrNot[1] = True
        firstOrNot[0] = False
    def goBack():
        if not(firstOrNot[1]) and firstOrNot[0]:
            amount = checkAllAmount(combox.get())
            if isinstance(amount, list):
                ctypes.windll.user32.MessageBoxW(0, '恭喜您總共中了' + amount[0] + 
                    '元\n扣稅後，總金額為' + amount[1] + '元', '{0}中獎金額'.format(combox.get()), 0)
            else:
                ctypes.windll.user32.MessageBoxW(0, amount, '{0}中獎金額'.format(combox.get()), 0)
        reciptList.destroy()
    reciptList = tkinter.Tk()
    reciptList.title('對未輸入發票')  
    center_window(reciptList, 400, 400)
    reciptList.resizable(width = False, height = False)
    reciptList.after(1, lambda: reciptList.focus_force())
    label1 = tkinter.Label(reciptList, text = '請選擇您要對發票的月份：', font = 30)
    label1.place(x = 5, y = 10)
    comvalue = tkinter.StringVar()
    combox = ttk.Combobox(reciptList, textvariable = comvalue, font = 30, state = 'readonly')
    firstOrNot = [False, False]; findFile = file('年'); comboxOption = []
    for fileName in findFile:
        if len(fileName) == 14:
            fileName = fileName.replace('.txt', '')
            comboxOption.append(fileName)
    combox["values"] = tuple(comboxOption)
    combox.current(0) if len(comboxOption) == 1 else combox.current(1)
    combox.bind("<<ComboboxSelected>>", confirmDate)
    combox.place(x = 5, y = 45)
    confirmDate(fileName)
    button3 = tkinter.Button(reciptList, text = "返回", font = 30, command = goBack)
    button3.place(x = 345, y = 365)
    reciptList.protocol('WM_DELETE_WINDOW', goBack)
    reciptList.mainloop()
def firstList(GUI):
    def goBack():
        firstList.destroy()
        mainList()
    GUI.destroy()
    firstList = tkinter.Tk()
    firstList.title("對發票")
    center_window(firstList, 400, 400)
    firstList.resizable(width = False, height = False)
    firstList.after(1, lambda: firstList.focus_force())
    button1 = tkinter.Button(firstList, text = "1)對之前已輸入發票", font = 30,  command = reciptLotteryAlready)
    button1.place(x = 5, y = 10)
    button2 = tkinter.Button(firstList, text = "2)對未輸入發票", font = 30, command = reciptLottery)
    button2.place(x = 5, y = 60)
    button3 = tkinter.Button(firstList, text = "3)返回", font = 30, command = goBack)
    button3.place(x = 5, y = 110)
    firstList.protocol('WM_DELETE_WINDOW', goBack)
    firstList.mainloop()
def getReceiptMon():
    localtime = time.localtime(time.time())
    year = str(localtime.tm_year - 1911)
    mon = localtime.tm_mon
    if mon % 2 == 1:
        n = year + '年' + str(mon).zfill(2) + '-' + str(mon + 1).zfill(2) + '月'
    else:
        n = year + '年' + str(mon - 1).zfill(2) + '-' + str(mon).zfill(2) + '月'
    return n
def secList(GUI):
    def goBack():
        secList.destroy()
        mainList()
    def confirmRecipt(event):
        s = True
        a = 'a' if os.path.isfile('{0}未開獎.txt'.format(fileName)) else 'x+'
        with open('{0}未開獎.txt'.format(fileName), a) as file1:
            if checkReceipt(entry.get()):
                s = False
                file1.write('{0}\n'.format(entry.get()))
                canvas.create_text(5, layout[0], text = entry.get(), font = 30, anchor = 'nw')
            else:
                canvas.create_text(5, layout[0], text = '輸入錯誤發票號碼', font = 30, anchor = 'nw')
            if layout[1] % 20 == 0: layout[2] += 500; canvas.config(scrollregion = (0, 0, 0, layout[2]))
            layout[0] += 25; layout[1] += 1
        if s and a == 'x+':
            os.remove('{0}未開獎.txt'.format(fileName))
        entry.delete(0, 'end')
    GUI.destroy()
    layout = [5, 1, 500]
    secList = tkinter.Tk()
    secList.title("輸入未開獎發票")
    center_window(secList, 400, 400)
    secList.resizable(width=False, height=False)
    secList.after(1, lambda: secList.focus_force())
    fileName = getReceiptMon()
    label1 = tkinter.Label(secList, text = fileName, font = 30)
    label1.place(x = 5, y = 10)
    label2 = tkinter.Label(secList, text = '請輸入您的發票號碼：', font = 30)
    label2.place(x = 5, y = 50)
    entry = tkinter.Entry(secList, font = 30)
    entry.place(x = 5, y = 90)
    entry.focus()
    entry.bind('<Return>', confirmRecipt)
    canvas = tkinter.Canvas(secList, width = 400, height = 230, scrollregion = (0, 0, 0, 500))
    vbar = tkinter.Scrollbar(canvas,orient='vertical', command = canvas.yview)
    vbar.place(x = 370, y = 0, width = 20, height = 230)
    canvas.config(yscrollcommand = vbar.set)
    canvas.place(x = 0, y = 130)
    button3 = tkinter.Button(secList, text = "返回", font = 30, command = goBack)
    button3.place(x = 345, y = 365)
    secList.protocol('WM_DELETE_WINDOW', goBack)
    secList.mainloop()
def checkDeleteNotLottery(sel, h):
    def goBack():
        checkList.destroy()
    def confirm(entry, canvas1):
        try:
            if os.path.isfile(receipt[2] + '未開獎.txt'):
                receiptlen = len(entry.get())
                if (receiptlen == 4 or receiptlen == 8):
                    deleteReceiptOrNot = False; receiptNumName = ''
                    for receiptNum in receipt[0]:
                        if entry.get() == receiptNum or entry.get() == receipt[0].get(receiptNum):
                            receiptNumName = receipt[0].get(receiptNum)
                            deleteReceiptOrNot = True
                            break
                    if deleteReceiptOrNot:
                        result = ctypes.windll.user32.MessageBoxW(0, '你確定是否刪除發票號碼: ' + receiptNumName, combox.get(), 1)
                        if result == 1:
                            del receipt[0][receiptNum]; canvas1.create_text(5, layout1[0], text = receiptNumName + ' 已刪除成功', font = 30, anchor = 'nw'); layout1[0] += 25
                            with open('{0}未開獎.txt'.format(combox.get()), 'w') as file1:
                                for receiptNum in receipt[0]: file1.writelines(receipt[0].get(receiptNum) + '\n')
                    else:
                        text1 = '在您的發票編號中，無此編號' if receiptlen == 4 else '在您的發票號碼中，無此號碼'
                        canvas1.create_text(5, layout1[0], text = text1, font = 30, anchor = 'nw'); layout1[0] += 25
                    if receipt[0] == dict(): os.remove('{0}未開獎.txt'.format(combox.get()))
                else:
                    canvas1.create_text(5, layout1[0], text = '輸入錯誤編號', font = 30, anchor = 'nw'); layout1[0] += 25
                if layout1[1] % 20 == 0: layout1[2] += 500; canvas1.config(scrollregion = (0, 0, 0, layout1[2]))
                layout1[1] += 1; confirmMonth(entry); entry.delete(0, 'end')
        except ValueError:
            entry.delete(0, 'end')
        except FileNotFoundError:
            entry.delete(0, 'end')
            canvas1.create_text(5, layout1[0], text = '已無{0}未開獎發票'.format(combox.get()), font = 30, anchor = 'nw')
    def confirmMonth(event):
        findFile = file('未開獎'); comboxOption = []
        for fileName in findFile:
            comboxOption.append(fileName.replace('未開獎.txt', ''))
        combox["values"] = tuple(comboxOption)
        if receipt[2] != combox.get():
            if not(sel): 
                layout1[0] = 10; layout1[1] = 1; layout1[2] = 500
                label2 = tkinter.Label(checkList, text = "請輸入您要刪除的編號", font = 30)
                label2.place(x = 5, y = 180)
                entry = tkinter.Entry(checkList, font = 30)
                entry.place(x = 5, y = 215)
                entry.focus()
                entry.bind('<Return>', lambda e: confirm(entry, canvas1))
                canvas1 = tkinter.Canvas(checkList, width = 400, height = 135, scrollregion = (0, 0, 0, 500))
                vbar1 = tkinter.Scrollbar(canvas1, orient = 'vertical')
                vbar1.place(x = 370, y = 0, width = 20, height = 130)
                vbar1.config(command = canvas1.yview)
                canvas1.config(yscrollcommand = vbar1.set)
                canvas1.place(x = 0, y = 235)
                receipt[2] = combox.get()
        canvas.delete('all'); fileName = combox.get(); i = 1; layout = [10, 1, 500]; z = dict(); a = []
        with open('{0}未開獎.txt'.format(fileName)) as file1:
            for line in file1.readlines():
                canvas.create_text(5, layout[0], text = '  ' + str(i).rjust(4, '0') + ': ' + line, font = 30, fill = 'darkblue', anchor = 'nw')
                if not(sel): z[str(i).rjust(4, '0')] = line.replace('\n', ''); a.append(z)
                if layout[1] % 20 == 0: layout[2] += 500; canvas.config(scrollregion = (0, 0, 0, layout[2]))
                layout[0] += 25; i += 1; layout[1] += 1
            if not(sel): receipt[0] = z; receipt[1] = i - 1
    receipt = [dict(), 0, '']
    checkList= tkinter.Tk()
    layout1 = [10, 1, 500]
    if sel:
        checkList.title('查看未開獎發票')
    else:
        checkList.title('刪除未開獎發票')
    center_window(checkList, 400, 400)
    checkList.resizable(width = False, height = False)
    checkList.after(1, lambda: checkList.focus_force())
    button1 = tkinter.Button(checkList, text = '返回', font = 30, command = goBack)
    button1.place(x = 345, y = 365)
    findFile = file('未開獎'); comboxOption = []
    if len(findFile) == 0:
        label1 = tkinter.Label(checkList, text = '您未輸入未開獎發票', font = 30)
        label1.place(x = 5, y = 10)
    else:
        label1 = tkinter.Label(checkList, text = '請選擇月份：', font = 30)
        label1.place(x = 5, y = 10)
        comvalue = tkinter.StringVar()
        combox = ttk.Combobox(checkList, textvariable = comvalue, font = 30, state = 'readonly')
        for fileName in findFile:
            comboxOption.append(fileName.replace('未開獎.txt', ''))
        combox["values"] = tuple(comboxOption)
        combox.current(0) if len(comboxOption) == 1 else combox.current(1)
        combox.bind("<<ComboboxSelected>>", confirmMonth)
        combox.place(x = 5, y = 40)
        canvas = tkinter.Canvas(checkList, width = 400, height = h, scrollregion = (0, 0, 0, 500))
        vbar = tkinter.Scrollbar(canvas, orient = 'vertical')
        vbar.place(x = 370, y = 0, width = 20, height = h)
        vbar.config(command = canvas.yview)
        canvas.config(yscrollcommand = vbar.set)
        canvas.place(x = 0, y = 70)
        confirmMonth(fileName)
    checkList.mainloop()
def thrList(GUI):
    def goBack():
        thrList.destroy()
        mainList()
    GUI.destroy()
    thrList = tkinter.Tk()
    thrList.title("查看未開獎發票")
    center_window(thrList, 400, 400)
    thrList.resizable(width = False, height = False)
    thrList.after(1, lambda: thrList.focus_force())
    button1 = tkinter.Button(thrList, text = '1)查看', font = 30, command = lambda: checkDeleteNotLottery(True, 300))
    button1.place(x = 5, y = 10)
    button2 = tkinter.Button(thrList, text = '2)刪除', font = 30, command = lambda: checkDeleteNotLottery(False, 100))
    button2.place(x = 5, y = 60)
    button3 = tkinter.Button(thrList, text = '3)返回', font = 30, command = goBack)
    button3.place(x = 5, y = 110)
    thrList.protocol('WM_DELETE_WINDOW', goBack)
    thrList.mainloop()
def fouList(GUI):
    def goBack():
        fouList.destroy()
        mainList()
    def confirmMonth(event):
        canvas.delete('all'); n = combox.get(); i = 1; layout = [10, 1, 500]
        canvas.config(scrollregion = (0, 0, 0, 500))
        label = tkinter.Label(fouList, text = n + '的中獎發票', font = 30)
        label.place(x = 5, y = 47)
        with open('{0}中獎發票.txt'.format(n)) as file1:
            for line in file1.readlines():
                canvas.create_text(10, layout[0], text = str(i).rjust(4, '0') + ': ' + line, font = 30, fill = "darkblue", anchor = 'nw')
                if layout[1] % 20 == 0: layout[2] += 500; canvas.config(scrollregion = (0, 0, 0, layout[2]))
                i += 1; layout[0] += 25; layout[1] += 1
    def winReceiptP(event):
        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            return "{:.2f}%\n({:d})".format(pct, absolute)
        labels = 'Winning', 'Not Winning'; labelsex = ['Special Prize', 'Particular Prize', 'First Prize', 'Second Prize', 'Third Prize', 'Fourth Prize', 'Fifth Prize', 'Sixth Prize', 'Add Sixth Prize']
        size = []; asize = []; labels1 = []; i = 0
        with open('{0}.txt'.format(combox1.get())) as file:
            for line in file.readlines():
                size.append(int(line)) if len(size) < 2 else asize.append(int(line))
        while(len(asize) > i):
            if asize[i] != 0:
                labels1.append(labelsex[i]); i += 1
            else:
                del asize[i]
        np.array(size); np.array(asize)
        fig = plt.figure()
        ax1 = fig.add_axes([.0, .1, .5, .8], aspect = 1)
        ax1.pie(size, labels = labels, autopct = lambda pct: func(pct, size), textprops = {"fontsize" : 12})
        ax2 = fig.add_axes([.45, .1, .5, .8], aspect = 1)
        ax2.pie(asize, labels = labels1, autopct = lambda pct: func(pct, asize), textprops = {"fontsize" : 12})
        ax1.set(aspect = "equal", title='Winning Probability')
        ax2.set(aspect = "equal", title='Winning Prize')
        plt.gcf().set_size_inches(16, 8)
        ax1.legend(labels,bbox_to_anchor=(1, 1.05), loc='best', borderaxespad=0.)
        ax2.legend(labels1,bbox_to_anchor=(0.92, 0.2), loc='best', borderaxespad=0.)
        plt.show()
    GUI.destroy()
    fouList = tkinter.Tk()
    fouList.title("查看中獎發票")
    center_window(fouList, 400, 400)
    fouList.resizable(width = False, height = False)
    fouList.after(1, lambda: fouList.focus_force())
    comvalue = tkinter.StringVar()
    combox = ttk.Combobox(fouList, textvariable = comvalue, font = 30, state = 'readonly')
    try:
        comvalue1 = tkinter.StringVar()
        combox1 = ttk.Combobox(fouList, textvariable = comvalue1, font = 30, state = 'readonly', width = 22)
        findFile = file('中獎機率'); comboxOption = []; qqqqq = 0
        for fileName in findFile:
            comboxOption.append(fileName.replace('.txt', ''))
        combox1["values"] = tuple(comboxOption)
        combox1.current(0) if len(comboxOption) == 1 else combox1.current(len(comboxOption) - 1)
        combox1.bind("<<ComboboxSelected>>", winReceiptP)
        combox1.place(x = 5, y = 16)
    except:
        qqqqq = 1
    findFile = file('中獎發票'); comboxOption = []
    if len(findFile) == 0:
        label1 = tkinter.Label(fouList, text = '還未有中獎發票', font = 30)
        label1.place(x = 5, y = 10) if qqqqq == 1 else label1.place(x = 5, y = 50)
    else:
        for fileName in findFile:
            comboxOption.append(fileName.replace('中獎發票.txt', ''))
        combox["values"] = tuple(comboxOption)
        combox.current(0) if len(comboxOption) == 1 else combox.current(len(comboxOption) - 1)
        combox.bind("<<ComboboxSelected>>", confirmMonth)
        combox.place(x = 5, y = 75)
        canvas = tkinter.Canvas(fouList, width = 400, height = 260, scrollregion = (0, 0, 0, 500))
        canvas.place(x = 0, y = 110)
        vbar = tkinter.Scrollbar(canvas, orient = 'vertical')
        vbar.place(x = 380, width = 20, height = 260)
        vbar.configure(command = canvas.yview)
        canvas.config(yscrollcommand = vbar.set)
        confirmMonth(fileName)
    button2 = tkinter.Button(fouList, text = "返回", font = 30, command = goBack)
    button2.place(x = 345, y = 365)
    fouList.protocol('WM_DELETE_WINDOW', goBack)
    fouList.mainloop()
def mainList():
    def end():
        result = ctypes.windll.user32.MessageBoxW(0, '你確定要關閉程式嗎?', '結束程式', 1)
        if result == 1:
            GUI.destroy()
    GUI = tkinter.Tk()
    GUI.title("發票小助手")
    center_window(GUI, 400, 400)
    GUI.resizable(width = False, height = False)
    GUI.after(1, lambda: GUI.focus_force())
    button1 = tkinter.Button(GUI, text = '1)對發票', font = 30, command = lambda: firstList(GUI))
    button1.place(x = 5, y = 10)
    button2 = tkinter.Button(GUI, text = '2)輸入未開獎發票', font = 30, command = lambda: secList(GUI))
    button2.place(x = 5, y = 60)
    button3 = tkinter.Button(GUI, text = '3)查看未開獎發票', font = 30, command = lambda: thrList(GUI))
    button3.place(x = 5, y = 110)
    button4 = tkinter.Button(GUI, text = '4)查看中獎發票', font = 30, command = lambda: fouList(GUI))
    button4.place(x = 5, y = 160)
    button5 = tkinter.Button(GUI, text = '5)結束', font = 30, command = end)
    button5.place(x = 5, y = 210)
    GUI.protocol('WM_DELETE_WINDOW', end)
    GUI.mainloop()
def receiptFile(num0, num1, f):
    localtime = time.localtime(time.time())
    year = localtime.tm_year - 1911; mon = localtime.tm_mon; day = localtime.tm_mday
    if num1 == "01":
        if not(((mon == 7 and day <= 5) or mon < 7) and year == num0):
            os.remove(f); return True
    elif num1 == "03":
        if not(((mon == 9 and day <= 5) or mon < 9) and year == num0):
            os.remove(f); return True
    elif num1 == "05":
        if not(((mon == 11 and day <= 5) or mon < 11) and year == num0):
            os.remove(f); return True
    elif num1 == "07":
        if not((mon == 10 and day >= 6 or mon > 10 and year == num0) or (mon == 1 and day <= 5 and year == num0 + 1)):
            os.remove(f); return True
    elif num1 == "09":
        if not((mon == 12 and day >= 6 and year == num0) or (mon == 3 and day <= 5 or mon < 3 and year == num0 + 1)):
            os.remove(f); return True
    elif num1 == "11":
        if not(((mon == 5 and day <= 5) or mon < 5) and year == num0 + 1):
            os.remove(f); return True
def checkOvertimeReceiptFile():
    files = os.listdir("./")
    for f in files:
        num = re.findall(r"\d+",f)
        if not(f.find('中獎發票') >= 0 or f.find('金額') >= 0 or f.find('中獎機率') >= 0):
            if len(num) == 3:
                num0 = int(num[0]); num1 = num[1]
                if receiptFile(num0, num1, f):
                    if f.find('未開獎') < 0:
                        ctypes.windll.user32.MessageBoxW(0, f.replace('\n', '').replace('.txt', '') + '的發票已過期', '過期發票', 0)
                    else:
                        ctypes.windll.user32.MessageBoxW(0, '您之前所輸入' + f.replace('\n', '').replace('.txt', '') + '的發票尚未對獎，但是已過期', '過期發票', 0)
    b = file('未開獎')
    if len(b) > 0:
        for f in files:
            for a in b:
                if a.replace('未開獎', '').find(f) >= 0:
                    ctypes.windll.user32.MessageBoxW(0, '您之前所輸入的發票號碼，' + f.replace('.txt', '') + '已開獎，請盡快對獎', '發票已開獎', 0)
def updateReceiptFile(url, receiptMon):
    r = requests.get(url=url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    sel = soup.select('span.font-weight-bold')
    with open('{0}.txt'.format(receiptMon), 'a') as file1:
        for i in range(0, len(sel)//2):
            if len(sel[i].text) == 5:
                winReceipt = sel[i].text + sel[i+1].text
                file1.writelines('{0}\n'.format(winReceipt))
            elif len(sel[i].text) == 8:
                winReceipt = sel[i].text
                file1.writelines('{0}\n'.format(winReceipt))
    file1.close()
def updateReceipt():
    try:
        r = requests.get(url="https://invoice.etax.nat.gov.tw/index.html")
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'html.parser')
        mon = soup.select(".carousel-item")
        receiptMon = (mon[0].text).replace('中獎號碼單', '')
        receiptMon1 = (mon[2].text).replace('中獎號碼單', '')
        if not(os.path.isfile('{0}.txt'.format(receiptMon))):
            updateReceiptFile("https://invoice.etax.nat.gov.tw/index.html", receiptMon)
        if not(os.path.isfile('{0}.txt'.format(receiptMon1))):
            updateReceiptFile("https://invoice.etax.nat.gov.tw/lastNumber.html", receiptMon1)
    except:
        ctypes.windll.user32.MessageBoxW(0, '目前無網際網路，無法更新檔案!', '無法更新', 0)
updateReceipt()
checkOvertimeReceiptFile()
mainList()