# 918/utils/assertion_handler.py

def execute_assertions(response_data, validation_rules):
    """
    根据提供的规则字典，对响应数据执行断言。
    这个函数检查业务错误码 'errno' 和错误信息 'errmsg'。

    :param response_data: API返回的JSON数据 (字典)
    :param validation_rules: 包含预期 'errno' 和 'errmsg' 的字典
    """
    assert response_data.get("errno") == validation_rules.get("errno"), \
        (f"断言失败: 字段'errno' 的值应该是 '{validation_rules.get('errno')}', "
         f"实际是 '{response_data.get('errno')}'")

    assert response_data.get("errmsg") == validation_rules.get("errmsg"), \
        (f"断言失败: 字段'errmsg' 的值应该是 '{validation_rules.get('errmsg')}', "
         f"实际是 '{response_data.get('errmsg')}'")