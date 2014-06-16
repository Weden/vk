# -*- coding: utf8 -*-
# Модуль для работы с API Вконтакте. Список методов API можно увидеть здесь https://vk.com/dev/methods.
#
# @author tz4678@gmail.com
import os
import re
import sys
import json
import time
import uuid
import urllib
import urllib2
import mimetypes
import webbrowser

class VKClientError(Exception):
    pass

class VKClient(object):
    def __init__(self, api_version=None, access_token=None, user_id=None, expires=None):
        self.api_version = api_version
        self.access_token = access_token
        self.user_id = user_id
        self.expires = expires
        self.user_agent = 'VKClient (Python %s.%s.%s)' % sys.version_info[:3]
        self.auth_url = 'https://oauth.vk.com/'
        self.api_url = 'https://api.vk.com/method/'
        self.delay_time = 0

    def auth(self, params, auth_type='authorize'):
        params['v'] = self.api_version
        self.encode_params(params)
        response = self.get_json(self.auth_url + auth_type + '?' + urllib.urlencode(params))
        if 'error' in response:
            if response['error'] == 'need_captcha':
                self.captcha_params(params, response)
                return self.auth(params)
            if response['error'] == 'need_validation' and 'redirect_uri' in response:
                webbrowser.open(response['redirect_uri'])
            raise VKClientError(response['error'] + ': ' + response['error_description'])
        self.access_token = response['access_token']
        if 'user_id' in response:
            self.user_id = response['user_id']
        if 'expires_in' in response and response['expires_in'] > 0:
            self.expires = time.time() + response['expires_in']

    def api(self, method, params={}):
        self.delay()       
        params['v'] = self.api_version
        if self.access_token:
            params['access_token'] = self.access_token
        self.encode_params(params)
        data = urllib.urlencode(params)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.get_json(self.api_url + method, data, headers)
        if 'error' in response:
            response = response['error']
            if response['error_code'] == 14:
                self.captcha_params(params, response)
                return self.api(method, params)
            raise VKClientError('API Error: %s - %s' % (response['error_code'], response['error_msg']))
        return response['response']

    def upload(self, upload_url, files):
        upload_url = str(upload_url)
        boundary = uuid.uuid4().hex
        data = []
        for name, path in files.items():
            if re.match('https?://', path, re.I):
                u = urllib.urlopen(path)
                content_type = u.info()['content-type']
                content = u.read()
            else:
                path = path.encode(sys.getfilesystemencoding())
                extension = os.path.splitext(path)[1]
                content_type = mimetypes.types_map[extension] if extension in mimetypes.types_map else 'application/octet-stream'
                f = open(path, 'rb')
                content = f.read()
                f.close()
            data.extend([
                '--' + boundary,
                'Content-Disposition: form-data; name="' + name + '"; filename="' + os.path.basename(path) + '"',
                'Content-Type: ' + content_type,
                '',
                content
            ])
        data.extend([
            '--' + boundary + '--',
            ''
        ])
        headers = {'Content-Type': 'multipart/form-data; boundary="' + boundary + '"'}
        data = '\r\n'.join(data)
        response = self.get_json(upload_url, data, headers)
        if 'error' in response:
            raise VKClientError('Upload Error: ' + response['error'])
        return response

    def delay(self):
        time.sleep(self.delay_time)

    def get_json(self, url, data=None, headers={}):
        headers.setdefault('User-Agent', self.user_agent)
        request = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(request)
            content = response.read()
        except urllib2.HTTPError, error:
            content = error.read()
        return json.loads(content.decode('utf8'))

    def process_captcha(self, url):
        raise VKClientError('Captcha needed')

    def captcha_params(self, params, response):
        params['captcha_key'] = self.process_captcha(response['captcha_img'])
        params['captcha_sid'] = response['captcha_sid']

    def encode_params(self, params):
        for k, v in params.items():
            if type(v) == unicode:
                params[k] = v.encode('utf8')