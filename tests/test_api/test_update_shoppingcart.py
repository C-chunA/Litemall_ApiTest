import allure
import yaml
from pathlib import Path
from utils.assertion_handler import execute_assertions

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
    def test_update_cart_item_number_success(self, logged_in_keywords, prepared_cart_item, logger):
        """
        测试场景：成功将购物车中一个商品的数量修改为5。
        """
        case_id = "update_success"
        logger.info(f"******************** 测试场景: {case_id} [开始] ********************")

        keywords = logged_in_keywords
        item_to_update = prepared_cart_item

        new_number = 5
        logger.info(f"准备将购物车条目ID {item_to_update['cart_item_id']} 的数量更新为 {new_number}")

        json_data = keywords.update_cart_item(
            id=item_to_update['cart_item_id'],
            goodsId=item_to_update['goodsId'],
            productId=item_to_update['productId'],
            number=new_number
        )

        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        expected_results = data['expected'][case_id]

        allure.attach(str(json_data), name="Update Success Response", attachment_type=allure.attachment_type.TEXT)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("业务码断言通过")

        logger.info("开始进行二次校验：查询购物车确认数量是否已更新")
        cart_data = keywords.query_shopping_cart()
        cart_list = cart_data.get('data', {}).get('cartList', [])
        found_updated_item = False
        for item in cart_list:
            if item.get('id') == item_to_update['cart_item_id']:
                assert item.get('number') == new_number
                found_updated_item = True
                logger.info(f"二次校验成功: 商品ID {item_to_update['cart_item_id']} 的数量已更新为 {new_number}")
                break
        assert found_updated_item, "二次校验失败：在购物车中未找到更新后的商品，或数量不正确"

        logger.info(f"******************** 测试场景: {case_id} [结束] ********************\n")