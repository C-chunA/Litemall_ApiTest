import allure
import pytest
from pathlib import Path

import yaml

from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

# --- 文件路径定义 ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'update_shoppingcart.yaml'


@allure.feature("Shopping Cart Operations")
class TestUpdateShoppingCart:
    """
    测试修改购物车中的商品。
    """

    @allure.story("Update Cart Item")
    @allure.title("测试成功修改购物车中商品的数量")
    def test_update_cart_item_number_success(self, logged_in_keywords, prepared_cart_item):
        """
        测试场景：成功将购物车中一个商品的数量修改为5。
        这个测试依赖 prepared_cart_item fixture 来准备前置数据。
        """
        # 1. 直接从 fixture 获取关键字对象和准备好的商品数据
        keywords = logged_in_keywords
        item_to_update = prepared_cart_item  # 包含了 id, goodsId, productId

        # 2. 定义要更新的新数量
        new_number = 5

        # 3. 调用修改数量的关键字
        json_data = keywords.update_cart_item(
            id=item_to_update['cart_item_id'],
            goodsId=item_to_update['goodsId'],
            productId=item_to_update['productId'],
            number=new_number
        )

        # 4. 加载预期结果并断言
        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        expected_results = data['expected']['update_success']

        allure.attach(str(json_data), name="Update Success Response", attachment_type=allure.attachment_type.TEXT)
        execute_assertions(json_data, expected_results)

        # 5. (可选但推荐) 再次查询购物车，进行更深层次的验证
        cart_data = keywords.query_shopping_cart()
        cart_list = cart_data.get('data', {}).get('cartList', [])
        found_updated_item = False
        for item in cart_list:
            if item.get('id') == item_to_update['cart_item_id']:
                assert item.get('number') == new_number
                found_updated_item = True
                break
        assert found_updated_item, "在购物车中未找到更新后的商品，或数量不正确"