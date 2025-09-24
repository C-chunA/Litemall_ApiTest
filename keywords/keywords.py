from api.api_endpoints import APIEndpoints

class Keywords:
    def __init__(self, base_url, logger):
        self.api = APIEndpoints(base_url, logger)
        self.logger = logger
        self.token = None

    def login(self, username, password):
        self.logger.info("--------- 关键字: login [开始] ---------")
        self.logger.info(f"输入参数: username='{username}', password='***'")
        data = {'username': username, 'password': password}
        response = self.api.call_interface('login', data=data)
        json_data = response.json()
        if response.status_code == 200 and json_data.get("errno") == 0:
            self.token = json_data.get("data", {}).get("token")
            self.logger.info("Token 已成功获取并存储")
        self.logger.info(f"返回结果: {json_data}")
        self.logger.info("--------- 关键字: login [结束] ---------")
        return json_data

    def get_user_info(self):
        self.logger.info("--------- 关键字: get_user_info [开始] ---------")
        if not self.token:
            raise PermissionError("用户未登录，请先调用 login 关键字。")
        auth_headers = {"x-litemall-token": self.token}
        response = self.api.call_interface('info', headers=auth_headers)
        json_data = response.json()
        self.logger.info(f"返回结果: {json_data}")
        self.logger.info("--------- 关键字: get_user_info [结束] ---------")
        return json_data

    def query_shopping_cart(self):
        self.logger.info("--------- 关键字: query_shopping_cart [开始] ---------")
        if not self.token:
            raise PermissionError("用户未登录，请先调用 login 关键字。")
        auth_headers = {"x-litemall-token": self.token}
        response = self.api.call_interface('query_shoppingcart_info', headers=auth_headers)
        json_data = response.json()
        self.logger.info(f"返回购物车商品数量: {len(json_data.get('data', {}).get('cartList', []))}")
        self.logger.info("--------- 关键字: query_shopping_cart [结束] ---------")
        return json_data

    def add_shopping_cart(self, goodsId, productId, number):
        self.logger.info("--------- 关键字: add_shopping_cart [开始] ---------")
        self.logger.info(f"输入参数: goodsId={goodsId}, productId={productId}, number={number}")
        if not self.token:
            raise PermissionError("用户未登录，请先调用 login 关键字。")
        request_data = {
            "goodsId": goodsId,
            "productId": productId,
            "number": number
        }
        auth_headers = {"x-litemall-token": self.token}
        response = self.api.call_interface('add_to_cart', data=request_data, headers=auth_headers)
        json_data = response.json()
        self.logger.info(f"返回结果: {json_data}")
        self.logger.info("--------- 关键字: add_shopping_cart [结束] ---------")
        return json_data

    def update_cart_item(self, id, goodsId, productId, number):
        self.logger.info("--------- 关键字: update_cart_item [开始] ---------")
        self.logger.info(f"输入参数: id={id}, goodsId={goodsId}, productId={productId}, number={number}")
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
        json_data = response.json()
        self.logger.info(f"返回结果: {json_data}")
        self.logger.info("--------- 关键字: update_cart_item [结束] ---------")
        return json_data

    def delete_cart_item(self, productIds):
        self.logger.info("--------- 关键字: delete_cart_item [开始] ---------")
        self.logger.info(f"输入参数: productIds={productIds}")
        if not self.token:
            raise PermissionError("用户未登录，无法删除购物车。")
        request_data = {"productIds": productIds}
        auth_headers = {"x-litemall-token": self.token}
        response = self.api.call_interface('delete_cart', data=request_data, headers=auth_headers)
        json_data = response.json()
        self.logger.info(f"返回结果 (最新的购物车列表): {json_data}")
        self.logger.info("--------- 关键字: delete_cart_item [结束] ---------")
        return json_data