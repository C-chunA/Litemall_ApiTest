import sys
import os
import pytest
from keywords.keywords import Keywords
# 不再需要直接导入 requests

# 1. 导入你项目中已有的 API 封装类
from api.api_endpoints import APIEndpoints

# 2. 保留项目路径设置，确保导入能够成功
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# 3. 提供现有的测试用例所依赖的 base_url fixture，确保兼容性
@pytest.fixture(scope='session')
def base_url(request):
    """
    从 pytest.ini 配置文件中读取 base_url。
    这是你现有测试用例 (test_cases.py) 运行所必需的 fixture。
    """
    return request.config.getini('base_url')


# 4. 提供一个基于项目中 APIEndpoints 的基础客户端 fixture
@pytest.fixture(scope="function")
def api_endpoints_client(base_url):
    """
    返回一个你项目中 APIEndpoints 类的实例。
    这是所有 API 交互的基础。
    """
    return APIEndpoints(base_url=base_url)


@pytest.fixture(scope="session")
def logged_in_keywords(base_url):
    """
    提供一个已经实例化并成功登录的 Keywords 对象。
    专用于关键字驱动的测试用例。
    """
    # 步骤一：创建 "服务生" 实例
    keywords = Keywords(base_url)

    # 步骤二：自动执行登录动作
    login_response = keywords.login("user123", "user123")

    # 步骤三：检查登录是否成功，如果失败，后续测试就没意义了
    assert login_response.get("errno") == 0, "【Fixture 前置失败】：用户登录失败，无法继续执行测试"

    # 步骤四：返回这个已经准备好的、登录过的 "服务生"
    yield keywords

    # (yield 之后可以添加测试结束后的清理代码，这里暂时不需要)


# 位于 918/tests/conftest.py

# ... (其他 fixture 保持不变) ...

@pytest.fixture(scope="function")
def prepared_cart_item(logged_in_keywords):
    """
    一个高级 fixture，它会自动完成以下事情：
    1. 登录 (复用 logged_in_keywords)。
    2. 添加一个固定的“测试专用商品”到购物车。
    3. 查询购物车，找到该商品的 id 和 productId。
    4. 将这两个 ID `yield` 给测试函数。
    5. 测试结束后，自动删除该商品，清理环境。
    """
    keywords = logged_in_keywords

    # --- 前置准备 (Setup) ---
    # 定义一个我们用来测试的商品
    test_goodsId = 1009024
    test_productId = 16
    test_number = 1

    # 先尝试删除一次，确保购物车里没有这个商品，避免干扰
    keywords.delete_cart_item(productIds=[test_productId])

    # 添加“测试专用商品”
    add_response = keywords.add_shopping_cart(test_goodsId, test_productId, test_number)
    assert add_response.get("errno") == 0, "【Fixture 前置失败】：添加测试商品失败"

    # 查询购物车，找到我们刚刚添加的商品
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

    # --- 提供数据给测试 (`yield`) ---
    # 将包含多个值的字典 yield 出去，测试函数可以直接使用
    yield {
        "cart_item_id": cart_item_id,
        "goodsId": test_goodsId,
        "productId": found_product_id
    }

    # --- 后置清理 (Teardown) ---
    # # 测试函数执行完毕后，这里的代码会自动执行
    print("\n--- 开始执行 Teardown 清理 ---")
    keywords.delete_cart_item(productIds=[found_product_id])
    print("--- Teardown 清理完成 ---")