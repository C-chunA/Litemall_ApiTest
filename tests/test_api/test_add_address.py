import allure
import pytest
from pathlib import Path
from keywords.keywords import Keywords
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'add_address.yaml'

@allure.feature("Address Management")
class TestAddAddress:

    @allure.story("Add to Address")
    @allure.title("测试成功新增收货地址")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)
    )
    def test_add_address(self, logged_in_keywords, logger, case_id, request_data, expected_results):
        """
        测试场景：新增地址并删除。
        """

        allure.dynamic.title(f"新增收货地址测试：{case_id}")

        logger.info(f"===== 开始执行添加收货地址测试场景: {case_id} =====")

        keywords = logged_in_keywords
        json_data = keywords.add_address(**request_data)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"===== 场景 {case_id} 测试通过 =====")

        # #清除数据
        if case_id == "add_address_success":
            address_id = json_data.get('data')
            logger.info(f"清除新增的地址：id: {address_id}")
            keywords.delete_address(address_id)