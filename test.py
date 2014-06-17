# -*- coding: utf8 -*-
from vkapp import *

username = '<username>'
password = '<password>'
vk = VKApp(5.21)
vk.login(username, password)
vk.api('wall.post', {'message': u'Тест #1'})
vk.choose_client('IPHONE')
vk.login(username, password)
vk.api('wall.post', {'message': u'Тест #2'})