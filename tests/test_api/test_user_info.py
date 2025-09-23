import allure
import pytest
from pathlib import Path
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data  # 1. 導入通用加載器

# --- 文件路徑定義 (保持不變) ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'user_info.yaml'


@allure.feature("User Management")
class TestUserInfo:

    @allure.story("Get User Information")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)  # 2. 直接調用通用加載器
    )
    def test_get_user_info_scenarios(self, logged_in_keywords, case_id, request_data, expected_results):
        allure.dynamic.title(f"【關鍵字驅動】獲取用戶信息測試：{case_id}")

        keywords = logged_in_keywords
        json_data = keywords.get_user_info()  # 此接口無請求參數
        allure.attach(str(json_data), name=f"Response for {case_id}", attachment_type=allure.attachment_type.TEXT)
        execute_assertions(json_data, expected_results)