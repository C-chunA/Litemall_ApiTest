from api.api_endpoints import APIEndpoints
import logging

class Keywords:
    def __init__(self, base_url):
        self.api = APIEndpoints(base_url)
        self.logger = logging.getLogger('Keywords')
        self.token = None  # 1. 在这里，我们给“服务生”一个名叫 token 的空口袋

    def login(self, username, password):
        data = {'username': username, 'password': password}
        response = self.api.call_interface('login', data=data)
        self.logger.info("Login keyword executed")
        json_data = response.json()
        # print(json_data)
        # token = json_data['data']['token']  # 或 .get('data', {}).get('token')

        # 2. 如果登录成功，就把 token 放进 self.token 这个口袋里
        if response.status_code == 200 and json_data.get("errno") == 0:
            self.token = json_data['data']['token']

        return json_data

    def get_user_info(self):
        """
        获取用户信息的关键字。
        这是一个 GET 请求，同样需要认证。
        """
        # 检查是否已经登录
        if not self.token:
            raise PermissionError("用户未登录，请先调用 login 关键字。")

        # 准备包含 token 的请求头
        auth_headers = {"x-litemall-token": self.token}

        # 调用底层的 'info' 接口，并传入认证信息
        response = self.api.call_interface('info', headers=auth_headers)
        return response.json()

    def query_resource(self, resource_id):
        params = {'id': resource_id}
        response = self.api.call_interface('query', params=params)
        self.logger.info("Query keyword executed")
        return response.json()

    def add_shopping_cart(self, goodsId, productId, number):
        """
        添加商品到购物车的关键字。
        """

        # 准备请求需要的数据
        request_data = {
            "goodsId": goodsId,
            "productId": productId,
            "number": number
        }
        # 准备包含 token 的请求头
        auth_headers = {"x-litemall-token": self.token}

        # 调用底层接口，并把认证信息传进去
        response = self.api.call_interface('add_to_cart', data=request_data, headers=auth_headers)
        return response.json()

    def query_shopping_cart(self):
        """
        获取购物车信息的关键字。
        这是一个 GET 请求，同样需要认证。
        """

        # 准备包含 token 的请求头
        auth_headers = {"x-litemall-token": self.token}

        # 调用底层的 'query_shoppingcart_info' 接口，并传入认证信息
        response = self.api.call_interface('query_shoppingcart_info', headers=auth_headers)
        print(response.json())
        return response.json()

    def update_cart_item(self, id, goodsId, productId, number):
        """
        修改购物车中商品的数量。
        """
        if not self.token:
            raise PermissionError("用户未登录，无法修改购物车。")

        request_data = {
            "id": id,
            "goodsId": goodsId,
            "productId": productId,
            "number": number
        }
        auth_headers = {"x-litemall-token": self.token}
        response = self.api.call_interface('update_cart', data=request_data, headers=auth_headers)
        return response.json()

    def delete_cart_item(self, productIds):
        """
        从购物车中删除一个或多个商品。
        """
        if not self.token:
            raise PermissionError("用户未登录，无法删除购物车。")

        request_data = {"productIds": productIds}  # 注意：参数是 productIds 列表
        auth_headers = {"x-litemall-token": self.token}
        response = self.api.call_interface('delete_cart', data=request_data, headers=auth_headers)
        return response.json()

