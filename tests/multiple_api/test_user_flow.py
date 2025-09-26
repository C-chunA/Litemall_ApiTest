import allure
import pytest

from keywords.keywords import Keywords


@allure.feature("Business Flow Tests")
class TestUserFlow:
    """
    包含用户登录-查看用户信息-用户登出流程
    """

    @allure.story("Full User Lifecycle")
    @allure.title("测试完整的用户流程：登录 -> 查看用户信息 -> 登出")
    def test_full_user_scenario(self,base_url,logger):

        keyword = Keywords(base_url, logger)
        case_id = "full_user_flow"
        logger.info(f"******************** 业务流程测试: {case_id} [开始] ********************")

        username = 'user123'
        password = 'user123'

        # --- 步骤 1: 登录 ---
        login_response =keyword.login(username, password)
        assert login_response.get("errno") == 0
        assert login_response.get("errmsg") == "成功"
        logger.info("断言通过：登录成功")

        # --- 步骤 2: 查看用户信息 ---
        userinfo_response = keyword.get_user_info()
        assert userinfo_response.get("errno") == 0
        assert userinfo_response.get("data",{})["nickName"] == username
        assert userinfo_response.get("errmsg") == "成功"
        logger.info("断言通过：查看用户信息成功，预期用户名：{username}，")

        # --- 步骤 3: 登出 ---
        logout_response = keyword.logout(username,password)
        assert logout_response.get("errno") == 0
        assert logout_response.get("errmsg") == "成功"
        logger.info("断言通过：登出成功")

        logger.info(f"===== 业务流程测试: {case_id} 执行完毕，完整用户流程验证通过 =====")
