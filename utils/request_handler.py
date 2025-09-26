import requests

class RequestHandler:
    def __init__(self, logger):
        self.logger = logger

    def get(self, url, params=None, headers=None):
        response = requests.get(url, params=params, headers=headers)
        self.logger.info(f"请求方式：GET {url} status： {response.status_code}")
        return response

    def post(self, url, data=None, json=None, headers=None):
        response = requests.post(url, data=data, json=json, headers=headers)
        self.logger.info(f"请求方式：POST 请求地址：{url}  status： {response.status_code}")
        return response