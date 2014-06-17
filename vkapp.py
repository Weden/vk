# -*- coding: utf8 -*
from vkclient import VKClient, VKClientError
from captcha import process_captcha

class VKApp(VKClient):
    def __init__(self, *args, **kwargs):
        super(VKApp, self).__init__(*args, **kwargs)
        self.process_captcha = process_captcha
        self.delay_time = 1.0 / 5
        self.set_client('android')

    def set_client(self, client=None):
        client = str(client).lower()
        # офиц приложение под android
        if client == 'android':
            self.client_id = 2274003
            self.client_secret = 'hHbZxrka2uZ6jB1inYsH'
        elif client == 'win8': # blocked
            self.client_id = 2692017
            self.client_secret = 'rqIkXYBauPjqE2EVxB2j'

    def login(self, username, password):
        self.auth({
            'username': username,
            'password': password,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'notify,friends,photos,audio,video,docs,notes,wall,groups,messages,notifications,activity,status,pages,stats',
            'grant_type': 'password'
        }, 'token')