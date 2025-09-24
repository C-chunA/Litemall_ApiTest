import logging

class LogAdapter(logging.LoggerAdapter):
    """
    这个 Adapter 用于在日志信息中动态插入 'test_case' 字段。
    """
    def process(self, msg, kwargs):
        # 拷贝一份上下文，避免污染 self.extra
        extra = self.extra.copy()

        # 如果 kwargs 里有额外的 extra，就合并进来
        if "extra" in kwargs:
            extra.update(kwargs["extra"])

        # 确保一定有 test_case 字段
        if "test_case" not in extra:
            extra["test_case"] = "general_context"

        # 写回 kwargs，保证 Formatter 能取到
        kwargs["extra"] = extra

        return msg, kwargs
