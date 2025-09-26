import allure
import pytest
from pathlib import Path
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data

# --- 文件路径定义 ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'user_info.yaml'


@allure.feature("User Management")
class TestUserInfo:
    """
    测试用户信息的获取功能。
    """

    @allure.story("Get User Information")
    @allure.title("获取用户信息")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)
    )
    def test_get_user_info_scenarios(self, logged_in_keywords, logger, case_id, request_data, expected_results):
        """
        一个函数覆盖所有获取用户信息的场景。
        """
        allure.dynamic.title(f"【关键字驱动】获取用户信息测试：{case_id}")

        logger.info(f"******************** 测试场景: {case_id} [开始] ********************")

        keywords = logged_in_keywords

        # 调用获取用户信息的关键字
        json_data = keywords.get_user_info()

        allure.attach(str(json_data), name=f"Response for {case_id}",
                      attachment_type=allure.attachment_type.TEXT)

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"******************** 测试场景: {case_id} [结束] ********************\n")