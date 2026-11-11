import time
from typing import Optional, List
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import get_logger

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)

    def find_element(self, by, value: str, timeout: float = 10.0):
        """Tìm 1 element có explicit wait."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements(self, by, value: str) -> List:
        """Tìm danh sách element không ném exception nếu rỗng."""
        return self.driver.find_elements(by, value)

    def click(self, by, value: str, timeout: float = 10.0):
        """Chờ element có thể click rồi thực hiện click."""
        el = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        el.click()
        self.logger.info(f"Đã click element ({by}: {value})")

    def is_visible(self, by, value: str, timeout: float = 5.0) -> bool:
        """Kiểm tra element có hiển thị hay không trong thời gian timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def take_screenshot(self, filepath: str):
        """Chụp ảnh màn hình thiết bị."""
        self.driver.save_screenshot(filepath)
        self.logger.info(f"Đã lưu ảnh màn hình: {filepath}")
