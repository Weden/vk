# -*- coding: utf8 -*-
from vkapp import *

app = VKApp(5.21)
app.login('<email>', '<password>')
print app.api('wall.post', {'message': u'Я хуй'})
