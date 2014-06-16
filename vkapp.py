# -*- coding: utf8 -*
from vkclient import VKClient, VKClientError
from captcha import process_captcha

class VKApp(VKClient):
    def __init__(self, *args, **kwargs):
        super(VKApp, self).__init__(*args, **kwargs)
        self.process_captcha = process_captcha
        # если приложение установлено у более чем 1 миллиона человек, то можно отправлять не более 35 запросов в секунду
        self.delay_time = 1.0 / 35

    def login(self, username, password):
        self.auth({
                       'username': username,
                       'password': password,
                       'client_id': 2274003,
                       'client_secret': 'hHbZxrka2uZ6jB1inYsH',
                       'scope': 'notify,friends,photos,audio,video,docs,notes,wall,groups,messages,notifications,activity,status,pages,stats',
                       'grant_type': 'password'
                  }, 
                  'token')