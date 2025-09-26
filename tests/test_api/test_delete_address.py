import allure
import pytest
import yaml
from pathlib import Path
from utils.assertion_handler import execute_assertions


# --- 文件路径定义 ---
TEST_DIR = Path(__file__).resolve().parent
DATA_FILE = TEST_DIR.parent.parent / 'data' / 'delete_address.yaml'


@allure.feature("Address Management")
class TestDeleteAddress:

    @allure.story("Delete Address")
    @allure.title("测试成功删除地址")
    def test_delete_address(self, logged_in_keywords, logger):
        """
        测试场景：成功删除新增的地址。
        """
        case_id = "delete_success"
        logger.info(f"******************** 测试场景: 删除收货地址 {case_id} [开始] ********************")  # 修正笔误

        keywords = logged_in_keywords

        # 新增地址（参数修正）
        add_response = keywords.add_address(
            addressDetail="殿下地铁站",
            areaCode="350203",
            city="厦门市",
            country="",
            county="思明区",
            isDefault=False,  # 修正为布尔值
            name="测试nama",
            postalCode="",
            province="福建省",
            tel="12309987656",
        )

        # 新增后先断言成功
        assert add_response.get("errno") == 0, f"新增地址失败：{add_response.get('errmsg')}"
        address_id = add_response.get('data')  # 用更清晰的变量名
        logger.info(f"准备删除收货地址，Id: {address_id}")  # 修正日志变量和笔误

        # 执行删除
        json_data = keywords.delete_address(id=address_id)

        # 读取预期结果并断言
        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        expected_results = data['expected'][case_id]

        logger.info(f"开始断言，预期结果: {expected_results}")
        execute_assertions(json_data, expected_results)
        logger.info("断言通过")

        logger.info(f"===== 测试场景: 删除收货地址 {case_id}  测试通过 =====")  # 修正笔误