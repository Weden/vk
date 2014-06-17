# -*- coding: utf8 -*
from vkclient import VKClient, VKClientError
from captcha import process_captcha

class VKApp(VKClient):
    def __init__(self, username=0, password=0, api_version=0, client='android'):
        super(VKApp, self).__init__(api_version)
        self.username = username
        self.password = password
        self.choose_client(client)
        self.process_captcha = process_captcha
        self.delay_time = 1.0 / 5

    def choose_client(self, client):
        client = client.lower()
        if client == 'android':
            self.client_id = 2274003
            self.client_secret = 'hHbZxrka2uZ6jB1inYsH'
        elif client == 'iphone':
            self.client_id = 3140623
            self.client_secret = 'VeWdmVclDCtn6ihuP1nt'
        else:
            raise Exception('Unknown client')

    def login(self):
        self.auth({
            'username': self.username,
            'password': self.password,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'password'
        }, 'token')

    def change_client(self, client):
        self.choose_client(client)
        self.login()