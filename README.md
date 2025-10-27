Litemall API 自动化测试框架

本项目是一个基于 Python + Pytest 构建的 API 自动化测试框架，旨在对 Litemall 电商平台的后端 API 进行自动化测试。

✨ 主要特性

分层架构: 清晰的目录结构，将测试用例、业务逻辑、API 封装、工具类和测试数据分离。

关键字驱动: 业务逻辑被封装在 keywords/keywords.py 中，使测试用例更易读、更贴近业务。

数据驱动: 使用 YAML 文件管理测试数据 (data/ 目录)，并通过 utils/data_loader.py 实现参数化测试。

强大的 Fixture 管理: 利用 tests/conftest.py 管理测试环境，自动处理登录 (logged_in_keywords)、接口关联的测试准备和清理 (prepared_cart_item, prepared_orderid)。

详细的日志系统: 通过 pytest.ini 配置，实现日志同时输出到控制台和按天归档的文件 (logs/YYYY-MM-DD.log)，并使用 utils/logger.py 中的 LogAdapter 自动添加测试用例上下文。

精美的测试报告: 集成 Allure 框架，生成详细、可视化的测试报告。

灵活的测试执行: 支持通过 pytest mark 标记 (pytest.ini 中定义) 来筛选运行特定模块或优先级的测试用例。

📁 项目结构

Litemall_ApiTest/
├── api/                  # API 接口封装层 (调度员)
│   └── api_endpoints.py
├── data/                 # 测试数据 (YAML 文件)
│   ├── add_shoppingcart.yaml
│   ├── test_data.yaml
│   └── ...
├── keywords/             # 业务关键字层 (核心业务逻辑)
│   └── keywords.py
├── logs/                 # 日志文件存储目录 (自动生成)
├── tests/                # 测试脚本目录
│   ├── conftest.py       # Pytest Fixtures 配置文件 (环境准备与清理)
│   ├── test_api/         # 存放单接口测试用例
│   │   ├── test_add_shopptcart.py
│   │   └── ...
│   └── multiple_api/     # 存放多接口流程测试用例
│       └── test_cart_flow.py
├── utils/                # 通用工具类
│   ├── assertion_handler.py # 通用断言
│   ├── data_loader.py    # YAML 数据加载器
│   ├── logger.py         # 日志 Adapter
│   └── request_handler.py # 底层 HTTP 请求发送
├── .gitignore            # Git 忽略文件配置
├── pytest.ini            # Pytest 配置文件 (包含日志、标记、基础 URL 等)
└── requirements.txt      # 项目依赖库 (需要手动创建)


🚀 快速开始

1. 环境准备

确保已安装 Python 3.x。

克隆本项目到本地。

重要: 在项目根目录下创建 requirements.txt 文件 (如果尚未创建)，并填入以下内容：

pytest
requests
PyYAML
allure-pytest
pytest-html
pytest-base-url
pytest-metadata


在项目根目录下，使用终端安装所需的依赖库：

pip install -r requirements.txt


确保本地已安装并配置好 Allure 命令行工具（用于生成报告）。

2. 配置

主要的配置项位于 pytest.ini 文件中：

base_url: 设置被测 API 的基础 URL。

markers: 注册自定义的 Pytest 标记 (例如 shopping_cart, login)，用于筛选测试用例。

日志相关的配置 (log_cli_*, log_file_*)，包括日志格式、级别和文件路径。

3. 运行测试

在项目根目录下，使用终端执行以下命令：

运行所有测试:

pytest


或者，显示更详细的输出：

pytest -v


只运行特定模块的测试 (使用 mark):
例如，只运行所有关于购物车的测试：

pytest -m shopping_cart


只运行登录相关的测试：

pytest -m login


运行特定文件或函数:

# 运行指定文件
pytest tests/test_api/test_add_shopptcart.py

# 运行指定文件中的特定类
pytest tests/test_api/test_add_shopptcart.py::TestShoppingCart

# 运行指定类中的特定函数 (注意参数化会展开)
pytest tests/test_api/test_add_shopptcart.py::TestShoppingCart::test_add_to_cart_scenarios[add_success]


4. 生成并查看 Allure 报告

运行测试并生成 Allure 结果:

# --alluredir 指定 Allure 结果文件的存储目录
pytest --alluredir=./allure-results


启动 Allure 服务查看报告:

allure serve ./allure-results


Allure 会在你的默认浏览器中打开一个本地服务，展示精美的测试报告。

📝 如何添加新的测试

定义接口: 在 data/ 目录下相关的 YAML 文件中，interfaces 部分添加新接口的 URL、方法等信息。

准备测试数据: 在 data/ 目录下对应的 YAML 文件中：

对于参数化测试，在 test_cases 部分添加不同场景的输入数据，expected 部分添加对应的预期输出。

对于依赖Fixture的单场景测试（如修改、删除），test_cases 可以为空或省略，只需在 expected 中定义预期结果。

封装业务关键字: 在 keywords/keywords.py 中添加新的方法，封装调用新接口的业务逻辑，并添加必要的日志记录 (self.logger.info(...))。

编写测试用例: 在 tests/test_api/ 或 tests/multiple_api/ 目录下创建新的 test_*.py 文件或在现有文件中添加新的测试函数。

单接口参数化测试: 模仿 test_add_shopptcart.py 的结构，使用 @pytest.mark.parametrize 和 load_yaml_test_data。记得在函数参数中加入 logger。

依赖Fixture的测试: 模仿 test_update_shoppingcart.py 的结构，在函数参数中请求需要的 Fixture (如 prepared_cart_item) 和 logger。

流程测试: 模仿 test_cart_flow.py 的结构，在一个函数内按顺序调用多个关键字。记得在函数参数中加入 logger。

添加标记 (可选): 在测试类或函数上方添加 @pytest.mark.<your_mark> 标签，并在 pytest.ini 中注册。

🤝 贡献

欢迎提出 Issue 或 Pull Request 来改进此框架。