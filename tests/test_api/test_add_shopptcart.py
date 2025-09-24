import allure
import pytest
from pathlib import Path
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'add_shoppingcart.yaml'


@allure.feature("Shopping Cart Management")
class TestShoppingCart:

    @allure.story("Add to Cart")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)
    )
    def test_add_to_cart_scenarios(self, logged_in_keywords, logger, case_id, request_data, expected_results):
        allure.dynamic.title(f"【关键字驱动】购物车测试：{case_id}")

        logger.info(f"===== 开始执行添加购物车测试场景: {case_id} =====")

        keywords = logged_in_keywords

        # 请求参数的日志已经移到关键字内部，这里不再重复
        json_data = keywords.add_shopping_cart(**request_data)

        allure.attach(str(json_data), name=f"Response for {case_id}", attachment_type=allure.attachment_type.TEXT)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"===== 场景 {case_id} 测试通过 =====")