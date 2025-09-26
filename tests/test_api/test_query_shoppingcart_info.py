import allure
import pytest
from pathlib import Path
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

# --- 文件路径定义 ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'query_shoppingcart_info.yaml'

@pytest.mark.shopping_cart
@allure.feature("Shopping Cart Management")
class TestShoppingCartInfo:
    """
    测试查询购物车信息功能。
    """

    @allure.story("Query Cart Info")
    @allure.title("查询购物车信息的接口")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)
    )
    def test_get_shoppingcart_info_scenarios(self, logged_in_keywords, logger, case_id, request_data, expected_results):
        """
        一个函数覆盖所有查询购物车的场景。
        """
        allure.dynamic.title(f"【关键字驱动】查询购物车测试：{case_id}")

        logger.info(f"******************** 测试场景: {case_id} [开始] ********************")

        keywords = logged_in_keywords

        # 调用查询购物车的关键字
        json_data = keywords.query_shopping_cart()

        allure.attach(str(json_data), name=f"Response for {case_id}",
                      attachment_type=allure.attachment_type.TEXT)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"******************** 测试场景: {case_id} [结束] ********************\n")