# -*- coding: utf-8 -*-
import urllib2
from Tkinter import *
from PIL import ImageTk, Image
from StringIO import StringIO

def process_captcha(url, headers = {}):
    root = Tk()
    root.focus_force()
    root.title(u'Капча')
    var = StringVar()
    def quit():
        # если окно было закрыто, а не отправлено, сбрасываем переменную
        var.set('')
        root.destroy()
    root.protocol('WM_DELETE_WINDOW', quit)
    # загружаем картинку
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    # создаем файловый объект из строки
    data = StringIO(response.read())
    # конвертируем его в формат с которым может работать Tkinter
    photo = ImageTk.PhotoImage(Image.open(data))
    # создаем label в котором будем отображать капчу
    label = Label(root, image=photo)
    label.pack()
    # добавляем поле ввода и делаем фокус на нем
    entry = Entry(root, width=10, textvariable=var)
    entry.pack()
    entry.focus()
    def on_enter(event):
        root.destroy()
    # добавляем событие по нажатию клавиши Enter
    entry.bind('<Return>', on_enter)
    # добавляем кнопку подтверждения
    submit = Button(root, text='Submit', command=root.destroy)
    submit.pack()
    # запускаем цикл и ждем его остановки
    root.mainloop()
    # возвращаем значение
    return var.get()