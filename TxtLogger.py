import os
import datetime
import atexit


class TxtLogger:
    """
    加强版 Logger：支持颜色输出、自动关闭、Print风格传参，文件名带时间戳
    """

    def __init__(self, log_dir, log_filename="train", log_extension="txt", log_to_console=True):
        self.log_dir = log_dir
        self.log_to_console = log_to_console

        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)

        # 生成带时间戳的文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if log_filename:
            log_filename = f"{log_filename}_{timestamp}.{log_extension}"
        else:
            log_filename = f"{timestamp}.{log_extension}"

        self.log_path = os.path.join(log_dir, log_filename)

        # 使用 line buffering (buffering=1) 可以在写入一行后尽可能快地刷新，
        # 但为了性能通常保持默认，并在 _write 中手动 flush
        self.file = open(self.log_path, "a+", encoding="utf-8")

        # 注册退出时的清理函数，比 __del__ 更靠谱
        atexit.register(self._close)

        # 记录日志文件创建
        self.info(f"日志文件创建: {self.log_path}")

    def _timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _format(self, *args):
        return " ".join(str(a) for a in args)

    def _write(self, level, *args):
        msg = self._format(*args)
        ts = self._timestamp()

        # 1. 写入文件 (纯文本，不带颜色)
        # 格式: [时间] [级别] 消息
        file_text = f"[{ts}] [{level}] {msg}"

        if hasattr(self, 'file') and not self.file.closed:
            self.file.write(file_text + "\n")
            self.file.flush()  # 确保不丢日志，实时写入磁盘

        # 2. 打印到控制台 (带颜色)
        if self.log_to_console:
            # ANSI 颜色代码
            colors = {
                "INFO": "\033[92m",  # 绿色
                "WARNING": "\033[93m",  # 黄色
                "ERROR": "\033[91m"  # 红色
            }
            reset = "\033[0m"
            color_code = colors.get(level, "")

            # 控制台输出带颜色的格式
            console_text = f"[{ts}] {color_code}[{level}]{reset} {msg}"
            print(console_text)

    def info(self, *args):
        """记录 INFO 级别的日志"""
        self._write("INFO", *args)

    def warning(self, *args):
        """记录 WARNING 级别的日志"""
        self._write("WARNING", *args)

    def error(self, *args):
        """记录 ERROR 级别的日志"""
        self._write("ERROR", *args)

    def _close(self):
        """关闭文件句柄"""
        if hasattr(self, 'file') and not self.file.closed:
            print(f"正在关闭日志文件: {os.path.abspath(self.log_path)}")
            self.file.close()

    def get_log_path(self):
        """获取日志文件完整路径"""
        return os.path.abspath(self.log_path)


