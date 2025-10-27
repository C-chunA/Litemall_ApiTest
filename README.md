
# Litemall API 自动化测试框架

本项目是一个基于 Python + Pytest 构建的 API 自动化测试框架，旨在对 Litemall 电商平台的后端 API 进行自动化测试。


## ✨ 核心特性

- **分层架构设计**：清晰的目录结构，将测试用例、业务逻辑、API 封装、工具类和测试数据分离，便于维护。
- **关键字驱动**：业务逻辑封装在 `keywords/keywords.py` 中，使测试用例更易读、贴近业务场景。
- **数据驱动**：通过 YAML 文件（`data/` 目录）管理测试数据，结合 `utils/data_loader.py` 实现参数化测试。
- **强大的 Fixture 管理**：通过 `tests/conftest.py` 处理测试环境准备与清理（如登录状态维持、测试数据预置）。
- **详细日志系统**：日志同时输出到控制台和按天归档的文件（`logs/YYYY-MM-DD.log`），自动关联测试用例上下文。
- **可视化测试报告**：集成 Allure 框架，生成包含步骤、截图、日志的详细报告。
- **灵活的测试执行**：支持通过 pytest 标记（`pytest.ini` 定义）筛选特定模块或优先级的测试用例。


## 📁 项目结构

```
Litemall_ApiTest/
├── api/                  # API 接口封装层（调度器）
│   └── api_endpoints.py  # 统一管理接口 URL、方法等配置
├── data/                 # 测试数据（YAML 文件）
│   ├── add_shoppingcart.yaml  # 购物车相关测试数据
│   ├── test_data.yaml          # 登录等基础测试数据
│   └── ...
├── keywords/             # 业务关键字层（核心逻辑）
│   └── keywords.py       # 封装接口调用的业务方法（如登录、下单）
├── logs/                 # 日志文件存储目录（自动生成）
├── tests/                # 测试脚本目录
│   ├── conftest.py       # Pytest Fixtures 配置（环境准备与清理）
│   ├── test_api/         # 单接口测试用例
│   │   ├── test_add_shopptcart.py  # 购物车添加测试
│   │   └── ...
│   └── multiple_api/     # 多接口流程测试用例
│       └── test_cart_flow.py  # 购物车完整流程测试
├── utils/                # 通用工具类
│   ├── assertion_handler.py  # 通用断言方法
│   ├── data_loader.py    # YAML 数据加载器
│   ├── logger.py         # 日志适配器（添加测试用例上下文）
│   └── request_handler.py # 底层 HTTP 请求发送
├── .gitignore            # Git 忽略文件配置
├── pytest.ini            # Pytest 配置文件（基础 URL、标记、日志等）
└── requirements.txt      # 项目依赖库清单
```


## 🚀 快速开始

### 1. 环境准备

- 确保已安装 Python 3.x
- 克隆本项目到本地
- 在项目根目录创建 `requirements.txt`，填入以下内容：
  ```
  pytest
  requests
  PyYAML
  allure-pytest
  pytest-html
  pytest-base-url
  pytest-metadata
  ```
- 安装依赖库：
  ```bash
  pip install -r requirements.txt
  ```
- 安装 Allure 命令行工具（用于生成报告），参考 [Allure 官方文档](https://docs.qameta.io/allure/)


### 2. 配置

核心配置位于 `pytest.ini`：
- `base_url`：被测 API 的基础 URL（如 `http://112.126.74.187`）
- `markers`：自定义测试标记（如 `shopping_cart`、`login`），用于筛选测试用例
- 日志配置：控制台日志格式、级别等（文件日志由 `tests/conftest.py` 管理）


### 3. 运行测试

在项目根目录执行以下命令：

- 运行所有测试：
  ```bash
  pytest
  ```

- 显示详细输出：
  ```bash
  pytest -v
  ```

- 运行特定标记的测试（如购物车模块）：
  ```bash
  pytest -m shopping_cart
  ```

- 运行指定文件：
  ```bash
  pytest tests/test_api/test_add_shopptcart.py
  ```

- 运行指定文件中的类：
  ```bash
  pytest tests/test_api/test_add_shopptcart.py::TestShoppingCart
  ```

- 运行指定类中的特定函数（参数化场景）：
  ```bash
  pytest tests/test_api/test_add_shopptcart.py::TestShoppingCart::test_add_to_cart_scenarios[add_success]
  ```


### 4. 生成并查看 Allure 报告

- 运行测试并生成 Allure 结果：
  ```bash
  pytest --alluredir=./allure-results
  ```

- 启动 Allure 服务查看报告：
  ```bash
  allure serve ./allure-results
  ```

Allure 会在默认浏览器中打开本地服务，展示包含测试步骤、日志、断言结果的可视化报告。


## 📝 如何添加新的测试

1. **定义接口**：在 `data/` 目录的 YAML 文件中，通过 `interfaces` 节点添加接口的 URL、方法、请求头：
   ```yaml
   interfaces:
     add_address:
       url: /wx/address/save
       method: POST
       headers:
         Content-Type: application/json
   ```

2. **准备测试数据**：在同一 YAML 文件中：
   - 通过 `test_cases` 节点定义参数化输入（如不同场景的请求参数）
   - 通过 `expected` 节点定义对应预期结果：
   ```yaml
   test_cases:
     add_success:
       name: "测试用户"
       tel: "13800138000"
   expected:
     add_success:
       errno: 0
       errmsg: 成功
   ```

3. **封装业务关键字**：在 `keywords/keywords.py` 中添加方法，封装接口调用逻辑（含日志记录）：
   ```python
   def add_address(self, name, tel, ...):
       self.logger.info("开始新增地址")
       # 构造请求数据、调用接口、返回响应
   ```

4. **编写测试用例**：在 `tests/test_api/` 或 `tests/multiple_api/` 目录下创建 `test_*.py` 文件：
   - **单接口参数化测试**：参考 `test_add_shopptcart.py`，使用 `@pytest.mark.parametrize` 和 `load_yaml_test_data`
   - **依赖 Fixture 的测试**：参考 `test_update_shoppingcart.py`，在函数参数中引用 Fixture（如 `logged_in_keywords`）
   - **流程测试**：参考 `test_cart_flow.py`，按顺序调用多个关键字实现业务流程

5. **添加标记（可选）**：在测试类/函数上添加 `@pytest.mark.<标记名>`，并在 `pytest.ini` 中注册标记。


## 🤝 贡献

欢迎通过 Issue 反馈问题或提交 Pull Request 改进框架。
