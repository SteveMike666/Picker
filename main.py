import requests
import bs4
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def get_news():
    def search():
        kw = e1.get()
        if len(kw.replace(" ", "")) == 0:
            messagebox.showwarning("新闻 - 警告", "搜索内容不能为空！", parent=win)
            return
        x = searchList.get_children()
        for item in x:
            searchList.delete(item)
        response = requests.get("https://36kr.com/search/articles/" + kw).text
        soup = bs4.BeautifulSoup(response, "lxml")
        data1 = soup.find_all(name="a", class_="article-item-title weight-bold")
        data2 = soup.find_all(name="a", class_="article-item-description ellipsis-2")
        for x in range(len(data1)):
            name = data1[x].text
            abstract = data2[x].text
            link = "https://36kr.com" + data1[x]["href"]

            searchList.insert("", x, values=(name, abstract, link))

    win = tk.Tk()
    win.title("小小新闻")
    win.geometry("800x500")
    win.resizable(False, False)

    l1 = tk.Label(win, text="小小新闻", font=(None, 40), fg="red")
    l1.pack()

    tk.Label(win).pack()

    frame1 = tk.Frame(win)

    e1 = ttk.Entry(frame1)
    e1.grid(row=0, column=0)
    e1.bind("<Return>", search)

    b1 = ttk.Button(frame1, text="搜索", command=search)
    b1.grid(row=0, column=1)

    frame1.pack()

    l4 = tk.Label(win, text="(以下内容来自36kr.com)")
    l4.pack()

    frame2 = tk.Frame(win)

    columns = ("标题", "摘要", "链接")
    columnWidths = (100, 250, 150)
    searchList = ttk.Treeview(frame2, show="headings", columns=columns, selectmode="browse")
    searchList.grid(row=0, column=0, ipadx=60, ipady=15)

    sb1 = tk.Scrollbar(frame2)
    sb1.grid(row=0, column=1, ipady=100)

    sb2 = tk.Scrollbar(frame2, orient="horizontal")
    sb2.grid(row=1, column=0, ipadx=260)

    searchList.config(yscrollcommand=sb1.set)
    searchList.config(xscrollcommand=sb2.set)
    sb1.config(command=searchList.yview)
    sb2.config(command=searchList.xview)

    for x in range(len(columns)):
        searchList.column(columns[x], anchor="center", width=columnWidths[x])
        searchList.heading(columns[x], text=columns[x])

    frame2.pack()

    frame3 = tk.Frame(win)

    def copytext(item):
        selection = searchList.item(searchList.focus())["values"]
        if selection == "":
            messagebox.showwarning("新闻 - 警告", "请选中要复制的那行！", parent=win)
            return
        win.clipboard_append(selection[item])

    b2 = ttk.Button(frame3, text="复制标题", command=lambda: copytext(0))
    b2.grid(row=0, column=0)

    b3 = ttk.Button(frame3, text="复制摘要", command=lambda: copytext(1))
    b3.grid(row=0, column=1)

    b4 = ttk.Button(frame3, text="复制链接", command=lambda: copytext(2))
    b4.grid(row=0, column=2)

    def openurl():
        selection = searchList.item(searchList.focus())["values"]
        if selection == "":
            messagebox.showwarning("新闻 - 警告", "请选中要打开链接的那行！", parent=win)
            return
        webbrowser.open(selection[2])

    b5 = ttk.Button(frame3, text="打开链接", command=openurl)
    b5.grid(row=0, column=3)

    frame3.pack()

    win.mainloop()
