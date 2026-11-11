import time
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class LiveVideoPage(BasePage):
    """Màn hình Live & Video Shopee."""

    INDICATOR_LOCATORS = [
        (AppiumBy.XPATH, "//*[@content-desc='click video comment_icon']"),
        (AppiumBy.XPATH, "//*[@content-desc='like vide']"),
        (AppiumBy.XPATH, "//*[@content-desc='click video share icon']"),
        (AppiumBy.XPATH, "//*[contains(@text, 'LIVE') or contains(@text, 'Live') or contains(@text, 'Mua ngay') or contains(@text, 'sản phẩm') or contains(@text, 'Thêm bình luận') or contains(@text, 'Chia sẻ')]")
    ]

    def is_displayed(self, timeout: float = 10.0) -> bool:
        """Kiểm tra màn hình Live & Video có hiển thị hay không."""
        self.logger.info("Xác thực màn hình Live & Video đang hiển thị...")
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            for by, val in self.INDICATOR_LOCATORS:
                elements = self.find_elements(by, val)
                if elements and any(e.is_displayed() for e in elements):
                    self.logger.info(f"Đã xác nhận vào màn hình Live & Video thành công (qua {by}={val}).")
                    return True
            time.sleep(0.5)

        self.logger.warning("Không tìm thấy phần tử Live & Video trong thời gian quy định.")
        return False
