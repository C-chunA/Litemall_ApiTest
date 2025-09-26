import allure
import pytest
from pathlib import Path
from keywords.keywords import Keywords
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'test_data.yaml'


@allure.feature("Authentication")
class TestAuth:

    @allure.story("User Login")
    @allure.title("测试成功登录")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)
    )
    def test_login_scenarios(self, base_url, logger, case_id, request_data, expected_results):
        """
        测试场景：成功登录。
        """
        allure.dynamic.title(f"【关键字驱动】登录测试：{case_id}")

        logger.info(f"===== 开始执行登录测试场景: {case_id} =====")

        keywords = Keywords(base_url, logger)

        json_data = keywords.login(**request_data)


        allure.attach(str(json_data), name=f"Response for {case_id}",
                      attachment_type=allure.attachment_type.TEXT)

        execute_assertions(json_data, expected_results)
        logger.info(f"===== 场景 {case_id} 测试通过 =====")