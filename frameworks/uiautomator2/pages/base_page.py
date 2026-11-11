import time
from typing import Optional
import uiautomator2 as u2
from utils.logger import get_logger

class BasePage:
    def __init__(self, device: u2.Device):
        self.d = device
        self.logger = get_logger(self.__class__.__name__)

    def wait_element(self, selector, timeout: float = 10.0) -> bool:
        """Chờ một phần tử xuất hiện trong khoảng thời gian timeout."""
        return selector.wait(timeout=timeout)

    def click(self, selector, timeout: float = 10.0):
        """Click vào phần tử sau khi chờ nó xuất hiện."""
        if selector.wait(timeout=timeout):
            selector.click()
            self.logger.info(f"Đã click phần tử: {selector}")
        else:
            raise TimeoutError(f"Hết thời gian chờ phần tử: {selector}")

    def take_screenshot(self, filepath: str):
        """Chụp ảnh màn hình hiện tại."""
        self.d.screenshot(filepath)
        self.logger.info(f"Đã lưu ảnh màn hình: {filepath}")
