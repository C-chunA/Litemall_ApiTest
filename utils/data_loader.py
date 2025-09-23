# 位於 918/utils/data_loader.py

import yaml
import pytest


def load_yaml_test_data(data_file_path):
    """
    一个通用的测试数据加载器。
    它可以读取指定的 YAML 文件，并将其整理成 pytest.mark.parametrize 需要的格式。

    :param data_file_path: YAML 文件的 Path 对象。
    :return: 一个包含 pytest.param 的列表。
    """
    with data_file_path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    test_data_list = []

    # 检查 YAML 文件中是否有 'test_cases'
    if 'test_cases' in data and data['test_cases']:
        # 遍历 'test_cases' 中的每一组数据
        for case_id, case_data in data['test_cases'].items():
            expected_results = data['expected'][case_id]
            test_data_list.append(pytest.param(case_id, case_data, expected_results, id=case_id))
    else:
        # 特殊处理像 user_info.yaml 这样没有参数的场景
        # 此时 'test_cases' 可能不存在或为空
        for case_id, expected_results in data['expected'].items():
            test_data_list.append(pytest.param(case_id, {}, expected_results, id=case_id))

    return test_data_list