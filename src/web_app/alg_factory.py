import urllib.request
import json

import requests


class factory:
    @staticmethod
    def make_request(href, js_arg):
        print(url+href)
        print(js_arg)
        answer = requests.post(url+href, json=js_arg)
        print(answer)
        response = answer.json()
        print(response)


url = 'http://localhost:8000/api/'
