# -*- coding: utf8 -*-
from vkapp import *

vk = VKApp('<username>', '<password>', 5.21)
# пробуем авторизоваться
vk.login()
vk.api('wall.post', {'message': u'Тест #1'})
vk.change_client('IPHONE')
vk.api('wall.post', {'message': u'Тест #2'})