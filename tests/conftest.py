import pytest
import logging
from pathlib import Path
from datetime import datetime  # 1. 导入 datetime 模块
from keywords.keywords import Keywords
from utils.logger import LogAdapter
from api.api_endpoints import APIEndpoints

# 定义一个全局变量来持有我们的文件处理器
file_handler = None


def pytest_configure(config):
    """
    在所有测试执行开始前，由 pytest 调用的钩子函数。
    我们在这里进行文件日志的全局配置。
    """
    global file_handler

    # 2. 动态生成文件名
    # 获取当前日期，格式化为 "YYYY-MM-DD"
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_dir = Path.cwd() / 'logs'
    log_dir.mkdir(exist_ok=True)
    # 文件名现在是动态的，例如：logs/2025-09-23.log
    log_file = log_dir / f"{current_date}.log"

    # 3. 创建一个文件处理器
    # 关键修改：mode='a' 代表 append (追加)，而不是 'w' (覆盖)
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')

    # 定义我们想要的日志格式
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - [%(test_case)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    # 获取根 logger，并将我们的文件处理器添加进去
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)


def pytest_unconfigure(config):
    """
    在所有测试执行结束后，由 pytest 调用的钩子函数。
    我们在这里进行清理工作。
    """
    global file_handler
    if file_handler:
        # 从根 logger 中移除我们的文件处理器
        logging.getLogger().removeHandler(file_handler)
        # 关闭文件句柄，确保所有缓存的日志都被写入文件
        file_handler.close()


# --- 以下所有 Fixtures 保持不变 ---

@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getini('base_url')


@pytest.fixture(scope='class')
def logger(request):
    """
    为每个测试用例创建一个带有上下文（测试用例名称）的 logger。
    """
    log_instance = logging.getLogger()
    test_case_name = request.node.name
    adapter = LogAdapter(log_instance, {'test_case': test_case_name})
    return adapter


@pytest.fixture(scope="class")
def logged_in_keywords(base_url, logger):
    keywords = Keywords(base_url, logger)
    login_response = keywords.login("user123", "user123")
    assert login_response.get("errno") == 0, "【Fixture 前置失败】：用户登录失败"
    yield keywords


@pytest.fixture(scope="function")
def prepared_cart_item(logged_in_keywords):
    keywords = logged_in_keywords
    test_goodsId = 1009024
    test_productId = 16
    test_number = 1

    keywords.delete_cart_item(productIds=[test_productId])
    add_response = keywords.add_shopping_cart(test_goodsId, test_productId, test_number)
    assert add_response.get("errno") == 0, "【Fixture 前置失败】：添加测试商品失败"

    cart_data = keywords.query_shopping_cart()
    cart_list = cart_data.get('data', {}).get('cartList', [])

    cart_item_id = None
    found_product_id = None
    for item in cart_list:
        if item.get('productId') == test_productId:
            cart_item_id = item.get('id')
            found_product_id = item.get('productId')
            break

    assert cart_item_id is not None, "【Fixture 前置失败】：在购物车中找不到测试商品"

    yield {
        "cart_item_id": cart_item_id,
        "goodsId": test_goodsId,
        "productId": found_product_id
    }

    print("\n--- 开始执行 Teardown 清理 ---")
    keywords.delete_cart_item(productIds=[found_product_id])
    print("--- Teardown 清理完成 ---")


# @pytest.fixture(scope="function")
# def prepared_orderid(logged_in_keywords):  #新增一个订单获取orderId，为删除订单准备数据
#     keywords = logged_in_keywords
#
#     test_addressid = 2
#     test_cartid = 3
#     test_couponid = ''
#     test_message = '取消订单准备的订单数据'
#
#     add_response = keywords.add_orders(test_addressid, test_cartid, test_couponid, test_message)
#
#     return add_response.get('data', {}).get('orderId')


