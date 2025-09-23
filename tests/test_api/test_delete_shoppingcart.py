import allure
import pytest
from pathlib import Path

import yaml

from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

# --- 文件路径定义 ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'delete_shoppingcart.yaml'


@allure.feature("Shopping Cart Operations")
class TestDeleteShoppingCart:
    """
    测试删除购物车中的商品。
    """

    @allure.story("Delete Cart Item")
    @allure.title("测试成功删除购物车中的商品")
    def test_delete_cart_item_success(self, logged_in_keywords, prepared_cart_item):
        """
        测试场景：成功删除一个由 fixture 准备好的商品。
        """
        # 1. 从 fixture 获取关键字对象和商品数据
        keywords = logged_in_keywords
        item_to_delete = prepared_cart_item

        # 2. 调用删除商品的关键字
        # 注意：删除接口需要的是一个包含 productId 的列表
        json_data = keywords.delete_cart_item(
            productIds=[item_to_delete['productId']]
        )

        # 3. 加载预期结果并断言
        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        expected_results = data['expected']['delete_success']

        allure.attach(str(json_data), name="Delete Success Response", attachment_type=allure.attachment_type.TEXT)
        execute_assertions(json_data, expected_results)

        # 4. (可选但推荐) 再次查询购物车，验证商品确实已被删除
        cart_data = json_data  # 删除接口的响应体就是最新的购物车列表
        cart_list = cart_data.get('data', {}).get('cartList', [])
        item_should_not_exist = False
        for item in cart_list:
            if item.get('productId') == item_to_delete['productId']:
                item_should_not_exist = True
                break
        assert not item_should_not_exist, "被删除的商品依然存在于购物车中"