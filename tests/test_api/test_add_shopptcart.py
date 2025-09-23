import allure
import pytest
from pathlib import Path
from utils.assertion_handler import execute_assertions
from utils.data_loader import load_yaml_test_data  # 1. 導入通用加載器

# --- 文件路徑定義 (保持不變) ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'add_shoppingcart.yaml'


@allure.feature("Shopping Cart Management")
class TestShoppingCart:

    @allure.story("Add to Cart")
    @pytest.mark.parametrize(
        "case_id, request_data, expected_results",
        load_yaml_test_data(DATA_FILE)  # 2. 直接調用通用加載器
    )
    def test_add_to_cart_scenarios(self, logged_in_keywords, case_id, request_data, expected_results):
        allure.dynamic.title(f"【關鍵字驅動】購物車測試：{case_id}")

        keywords = logged_in_keywords
        json_data = keywords.add_shopping_cart(**request_data) # 使用 ** 解包，更簡潔
        allure.attach(str(json_data), name=f"Response for {case_id}", attachment_type=allure.attachment_type.TEXT)
        execute_assertions(json_data, expected_results)