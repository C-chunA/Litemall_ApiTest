import allure
import pytest
from pathlib import Path
from keywords.keywords import Keywords
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'user_logout.yaml'


@allure.feature("Authentication")
class TestAuth:

    @allure.story("User Logout")
    @allure.title("测试成功登出")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)
    )
    def test_user_logout(self, logged_in_keywords,case_id, request_data, expected_results, logger,base_url):
        """
        测试场景：成功登出。
        """
        logger.info(f"===== 开始执行登出测试场景: {case_id} =====")

        keywords = logged_in_keywords


        json_data = keywords.logout(**request_data)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"===== 场景 {case_id} 测试通过 =====")
