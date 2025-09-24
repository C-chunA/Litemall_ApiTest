import yaml
from utils.request_handler import RequestHandler
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

class APIEndpoints:
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.request = RequestHandler(logger)
        self.config = {'interfaces': {}}
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".yaml"):
                file_path = DATA_DIR / filename
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if 'interfaces' in data:
                        self.config['interfaces'].update(data['interfaces'])

    def call_interface(self, interface_name, params=None, data=None, headers=None):
        config = self.config['interfaces'].get(interface_name)
        if not config:
            raise KeyError(f"在所有的 .yaml 配置文件中，都找不到名为 '{interface_name}' 的接口定义。")
        url = self.base_url + config['url']
        method = config['method'].lower()
        default_headers = config.get('headers', {})
        headers = {**default_headers, **(headers or {})}
        if method == 'get':
            return self.request.get(url, params=params, headers=headers)
        elif method == 'post':
            return self.request.post(url, json=data, headers=headers)