import allure
import pytest
import yaml
from pathlib import Path
from utils.assertion_handler import execute_assertions

# --- 文件路径定义 ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'delete_shoppingcart.yaml'

@pytest.mark.shopping_cart
@allure.feature("Shopping Cart Operations")
class TestDeleteShoppingCart:
    """
    测试删除购物车中的商品。
    """

    @allure.story("Delete Cart Item")
    @allure.title("测试成功删除购物车中的商品")
    def test_delete_cart_item_success(self, logged_in_keywords, prepared_cart_item, logger):
        """
        测试场景：成功删除一个由 fixture 准备好的商品。
        """
        case_id = "delete_success"
        logger.info(f"******************** 测试场景: {case_id} [开始] ********************")

        keywords = logged_in_keywords
        item_to_delete = prepared_cart_item

        logger.info(f"准备删除购物车中的商品，productId: {item_to_delete['productId']}")

        json_data = keywords.delete_cart_item(
            productIds=[item_to_delete['productId']]
        )

        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        expected_results = data['expected'][case_id]

        allure.attach(str(json_data), name="Delete Success Response", attachment_type=allure.attachment_type.TEXT)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("业务码断言通过")

        logger.info("开始进行二次校验：确认购物车中不再包含已删除的商品")
        cart_data = json_data
        cart_list = cart_data.get('data', {}).get('cartList', [])
        item_should_not_exist = False
        for item in cart_list:
            if item.get('productId') == item_to_delete['productId']:
                item_should_not_exist = True
                break
        assert not item_should_not_exist, f"二次校验失败：productId 为 {item_to_delete['productId']} 的商品依然存在于购物车中"
        logger.info(f"二次校验成功：商品 productId {item_to_delete['productId']} 已被成功删除")

        logger.info(f"******************** 测试场景: {case_id} [结束] ********************\n")