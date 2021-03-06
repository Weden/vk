# -*- coding: utf8 -*
from vkclient import VKClient, VKClientError
from captcha import process_captcha

class VKApp(VKClient):
    def __init__(self, api_version, client='android'):
        super(VKApp, self).__init__(api_version)
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

    def login(self, username, password):
        self.auth('token', {
            'username': username,
            'password': password,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'password'
        })