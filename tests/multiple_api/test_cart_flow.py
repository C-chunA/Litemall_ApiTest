import allure
import pytest


@allure.feature("Business Flow Tests")
@pytest.mark.shopping_cart
class TestCartFlow:
    """
    包含完整的业务流程测试用例，例如购物车的完整生命周期。
    """

    @allure.story("Full Cart Lifecycle")
    @allure.title("测试完整的购物车流程：添加 -> 修改 -> 删除")
    def test_full_cart_scenario(self, logged_in_keywords, logger):
        """
        测试一个商品的完整生命周期：
        1. 添加一个新商品到购物车。
        2. 验证商品已存在，并修改其数量。
        3. 验证数量已修改，并删除该商品。
        4. 验证商品已被删除。
        """
        keywords = logged_in_keywords
        case_id = "full_cart_flow"
        logger.info(f"******************** 业务流程测试: {case_id} [开始] ********************")

        # --- 定义测试用的商品数据 ---
        goods_id = 1009024
        product_id = 16
        initial_number = 1
        updated_number = 5

        # --- 环境清理：确保测试开始前，这个商品不在购物车里 ---
        logger.info("步骤0: 环境清理 - 确保测试商品不存在")
        keywords.delete_cart_item(productIds=[product_id])

        # --- 步骤 1: 添加商品到购物车 ---
        logger.info(f"步骤1: 添加商品到购物车 (productId: {product_id}, 数量: {initial_number})")
        add_response = keywords.add_shopping_cart(goods_id, product_id, initial_number)
        assert add_response.get("errno") == 0, "添加商品失败"
        logger.info("断言通过：添加商品成功")

        # --- 步骤 2: 查询购物车，获取动态ID，并准备修改 ---
        logger.info("步骤2: 查询购物车，获取动态生成的 cart_item_id")
        cart_data = keywords.query_shopping_cart()
        cart_list = cart_data.get('data', {}).get('cartList', [])

        cart_item_id = None
        item_found = False
        for item in cart_list:
            if item.get('productId') == product_id:
                cart_item_id = item.get('id')
                assert item.get('number') == initial_number
                item_found = True
                break

        assert item_found, f"在购物车中未找到刚刚添加的商品 (productId: {product_id})"
        logger.info(f"断言通过：商品已在购物车中，数量为 {initial_number}，获取到 cart_item_id: {cart_item_id}")

        # --- 步骤 3: 修改商品数量 ---
        logger.info(f"步骤3: 修改商品数量为 {updated_number}")
        update_response = keywords.update_cart_item(
            id=cart_item_id,
            goodsId=goods_id,
            productId=product_id,
            number=updated_number
        )
        assert update_response.get("errno") == 0, "修改商品数量失败"
        logger.info("断言通过：修改商品数量接口调用成功")

        # --- 步骤 4: 再次查询，二次校验修改结果 ---
        logger.info("步骤4: 二次校验 - 再次查询购物车确认数量已更新")
        cart_data_after_update = keywords.query_shopping_cart()
        cart_list_after_update = cart_data_after_update.get('data', {}).get('cartList', [])

        update_verified = False
        for item in cart_list_after_update:
            if item.get('id') == cart_item_id:
                assert item.get('number') == updated_number
                update_verified = True
                break

        assert update_verified, "二次校验失败：商品数量未成功更新"
        logger.info(f"断言通过：商品数量已成功更新为 {updated_number}")

        # --- 步骤 5: 删除商品 ---
        logger.info(f"步骤5: 从购物车中删除该商品 (productId: {product_id})")
        delete_response = keywords.delete_cart_item(productIds=[product_id])
        assert delete_response.get("errno") == 0, "删除商品失败"

        # --- 步骤 6: 最终校验，确认商品已被删除 ---
        logger.info("步骤6: 最终校验 - 确认购物车中已无该商品")
        final_cart_list = delete_response.get('data', {}).get('cartList', [])
        item_should_not_exist = False
        for item in final_cart_list:
            if item.get('productId') == product_id:
                item_should_not_exist = True
                break

        assert not item_should_not_exist, f"最终校验失败：被删除的商品 (productId: {product_id}) 依然存在"
        logger.info("断言通过：商品已成功从购物车中移除")

        logger.info(f"******************** 业务流程测试: {case_id} [结束] ********************\n")