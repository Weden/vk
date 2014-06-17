# -*- coding: utf8 -*-
from vkapp import *

vk = VKApp(5.21)
# маскируемся под офиц приложение для android
vk.choose_client('android')
vk.login('<email>', '<password>')
r = vk.api('wall.post', {'message': u'Тест'})
print r