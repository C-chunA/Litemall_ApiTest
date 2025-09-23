import yaml
from utils.request_handler import RequestHandler
import logging
from pathlib import Path
import os  # 1. 导入 os 库

# 定义项目的根目录
BASE_DIR = Path(__file__).resolve().parent.parent
# 定义数据文件所在的目录
DATA_DIR = BASE_DIR / 'data'


class APIEndpoints:
    def __init__(self, base_url):  # 2. 移除 data_file 参数
        self.base_url = base_url
        self.request = RequestHandler()
        self.logger = logging.getLogger('APIEndpoints')
        self.config = {'interfaces': {}}  # 3. 初始化一个空的配置字典

        # 4. 遍历 data 目录下的所有 .yaml 文件
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".yaml"):
                file_path = DATA_DIR / filename
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    # 如果文件中有 'interfaces' 键，就将其内容合并到主配置中
                    if 'interfaces' in data:
                        self.config['interfaces'].update(data['interfaces'])

    def call_interface(self, interface_name, params=None, data=None, headers=None):
        config = self.config['interfaces'].get(interface_name)

        # 增加一个健壮性检查，如果找不到接口，就抛出更明确的错误
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