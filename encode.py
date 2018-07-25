#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys

#编码库
import codecs
import chardet

#GUI库
from tkinter import *
import tkFileDialog

#根
root = Tk()
#搜索路径
searchPath = StringVar()
#目标编码
dstEncode = StringVar()
#文件字典-短路径
shortdic={}
#文件字典-长路径
longdic={}

# config
root.title("文件编码转换")
root.geometry('400x360')
root.resizable(width=False, height=False)

# ============= function =============
#检查反斜杠
def checkBackslash(path):
    return path.replace("\\","/")

#解析文件编码格式
def checkEnc(filename):
    with open(filename, 'rb') as fp:
        fp_read = fp.read()
        data = chardet.detect(fp_read)
        fp.close()
        return data

#转编码
def convert(filename, out_enc):
    try:
        f_read=codecs.open(filename,'r').read()
        source_encoding=chardet.detect(f_read)['encoding']
        u_data=f_read.decode(source_encoding)
        content=u_data.encode(out_enc)
        codecs.open(filename,'w').write(content)
    except IOError as err:
        t.insert(END, "I/O error:{0}".format(err)+"\n")
    except UnicodeError as err:
        t.insert(END, "Unicode error:{0}".format(err)+"\n")

#递归检查编码
def travCheckEnc(filepath):
    for file in os.listdir(filepath):
        path = os.path.join(filepath, file)
        path = checkBackslash(path)
        if os.path.isdir(path):
            travCheckEnc(path)
        if os.path.isfile(path):
            (shortname, extension) = os.path.splitext(file)
            if extension == ".cpp" or extension == ".h":
                result = checkEnc(path)
                index = len(shortdic) + 1
                shortdic[index] = result['encoding']
                t.insert(END, str(index)+". "+result['encoding']+"  |  "+file+"\n")

#递归转编码
def travConvertEnc(filepath, dstenc):
    for file in os.listdir(filepath):
        path = os.path.join(filepath, file)
        path = checkBackslash(path)
        if os.path.isdir(path):
            travConvertEnc(path, dstenc)
        if os.path.isfile(path):
            (shortname, extension) = os.path.splitext(file)
            if extension == ".cpp" or extension == ".h":
                convert(path, dstenc)

#搜索路径选择
def selectPath():
    path_ = tkFileDialog.askdirectory()
    searchPath.set(path_)

#检查编码
def checkAll():
    t.insert(END, "========================================="+"\n")
    if not searchPath.get():
        t.insert(END, "路径为空！"+"\n")
    else:
        shortdic.clear()
        t.insert(END, "检查中..."+"\n")
        travCheckEnc(searchPath.get())
        t.insert(END, "检查结束！"+"\n")
        t.see(END)
        finalCount()

#转编码
def transAll():
    t.insert(END, "========================================="+"\n")
    if not searchPath.get():
        t.insert(END, "路径为空！"+"\n")
    else:
        t.insert(END, "转编码中..."+"\n")
        t.see(END)
        travConvertEnc(searchPath.get(), dstEncode.get())
        t.insert(END, "转编码完成！"+"\n")
        t.see(END)

#检查编码完成统计
def finalCount():
    tmpdic = {}
    for cell in shortdic:
        if tmpdic.has_key(shortdic[cell]):
            tmpdic[shortdic[cell]] += 1
            pass
        else:
            tmpdic[shortdic[cell]] = 1
            pass
    t.insert(END, "----------------------------------\n")
    t.insert(END, str(tmpdic.keys())+"\n")
    t.insert(END, str(tmpdic.values())+"\n")
    t.see(END)

#清除文本显示内容
def clearLog():
    t.delete('1.0',END)

# ============= gui content =============
#路径选择
lbl = Label(root, text="目标路径:")
lbl.grid(row=0, column=0, sticky=W)
ety = Entry(root, textvariable = searchPath)
ety.grid(row=0, column=1, sticky=EW)
btnSelectPath = Button(root, text = "...", width=4, command = selectPath)
btnSelectPath.grid(row=0, column=2, sticky=E)

#内容显示
t = Text(root, width=54, height=20)
t.grid(row=1, column=0, columnspan=3, sticky=NSEW)
s=Scrollbar(root)
s.grid(row=1, column=3, columnspan=1, sticky=NS)
s.config(command=t.yview)
t.config(yscrollcommand=s.set)

#操作按钮
btnCheck = Button(root, text="检查编码", width=8, command = checkAll)
btnCheck.grid(row=2, column=0)
btnTrans = Button(root, text="转编码", width=8, command = transAll)
btnTrans.grid(row=2, column=1)
btnClear = Button(root, text="清除", width=8, command = clearLog)
btnClear.grid(row=2, column=2)

#转编码选项
rdbUTF8 = Radiobutton(root, text="UTF-8",variable=dstEncode,value='UTF-8')
rdbUTF8.grid(row=3, column=0)
rdbUTF8SIG = Radiobutton(root, text="UTF-8-with-BOOM",variable=dstEncode,value='UTF-8-SIG')
rdbUTF8SIG.grid(row=3, column=1)
rdbGB2312 = Radiobutton(root, text="GB2312",variable=dstEncode,value='GB2312')
rdbGB2312.grid(row=3, column=2)
dstEncode.set('UTF-8')

# ============= main =============
root.mainloop()