import allure
import pytest
from pathlib import Path
from keywords.keywords import Keywords
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data  # 1. 導入通用加載器

# --- 文件路徑定義 (保持不變) ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'test_data.yaml'


@allure.feature("Authentication")
class TestAuth:

    @allure.story("User Login")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)  # 2. 直接調用通用加載器
    )
    def test_login_scenarios(self, base_url, case_id, request_data, expected_results):
        allure.dynamic.title(f"【關鍵字驅動】登錄測試：{case_id}")

        keywords = Keywords(base_url)
        json_data = keywords.login(**request_data)
        allure.attach(str(json_data), name=f"Response for {case_id}", attachment_type=allure.attachment_type.TEXT)
        execute_assertions(json_data, expected_results)