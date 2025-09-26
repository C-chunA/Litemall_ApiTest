import allure
import pytest
import yaml
from pathlib import Path
from utils.assertion_handler import execute_assertions


# --- 文件路径定义 ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'delete_orders.yaml'


@allure.feature("Order Management")
class TestDeleteOrders:

    @allure.story("Delete Order")
    @allure.title("测试成功删除订单")

    def test_delete_orders(self, logged_in_keywords, logger):
        """
                测试场景：成功删除新增的订单。
        """
        case_id = "delete_success"
        logger.info(f"******************** 测试场景: 删除订单 {case_id} [开始] ********************")

        keywords = logged_in_keywords
        logger.info(f"前置操作：新增订单数据")
        add_response = keywords.add_orders(addressId = 2, cartId = 3 , couponId = '',
                                message = '取消订单准备的订单数据')
        orderId = add_response.get('data', {}).get('orderId')
        # orderId = prepared_orderid

        logger.info(f"准备删除订单，orderId: {orderId}")

        json_data = keywords.delete_orders(orderId=orderId)

        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        expected_results = data['expected'][case_id]

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"===== 测试场景: 删除订单 {case_id}  测试通过 =====")