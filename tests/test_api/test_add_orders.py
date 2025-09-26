import allure
import pytest
from pathlib import Path
from keywords.keywords import Keywords
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'add_orders.yaml'

@allure.feature("Order Management")
class TestAddOrders:

    @allure.story("Add to Orders")
    @allure.title("测试成功新增订单")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)
    )
    def test_add_orders(self, logged_in_keywords, logger, case_id, request_data, expected_results):
        """
        测试场景：成功创建订单并删除。
        """
        allure.dynamic.title(f"新增订单测试：{case_id}")

        logger.info(f"===== 开始执行添加订单测试场景: {case_id} =====")

        keywords = logged_in_keywords
        json_data = keywords.add_orders(**request_data)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"===== 场景 {case_id} 测试通过 =====")

        #清除数据
        if case_id == "add_success":
            orderId = json_data.get('data', {}).get('orderId')
            logger.info(f"清除新增的订单：orderId: {orderId}")
            keywords.delete_orders(orderId)