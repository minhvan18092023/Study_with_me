import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage
from .live_video_page import LiveVideoPage

class HomePage(BasePage):
    """Trang chủ Shopee trên Appium."""

    # Locators cho nút đóng Banner Sale / Popup
    BANNER_CLOSE_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'btn_close') or contains(@resource-id, 'button_close') or contains(@resource-id, 'iv_close') or contains(@resource-id, 'dialog_close')]"),
        (AppiumBy.XPATH, "//*[@text='✕' or @text='✖' or @text='X' or @text='x' or @text='Đóng' or @text='Close']"),
        (AppiumBy.XPATH, "//*[@content-desc='Đóng' or @content-desc='Close' or @content-desc='close' or @content-desc='dismiss']"),
        (AppiumBy.ID, "com.shopee.vn:id/button_close")
    ]

    # Locators cho tab Live & Video
    TAB_LIVE_VIDEO_LOCATORS = [
        (AppiumBy.XPATH, "//*[@content-desc='tab_bar_button_video_and_live']"),
        (AppiumBy.XPATH, "//*[@text='Live & Video']"),
        (AppiumBy.XPATH, "//*[contains(@text, 'Live') and contains(@text, 'Video')]")
    ]

    def dismiss_sale_banner_if_present(self, timeout: float = 4.0) -> bool:
        """Kiểm tra và click đóng banner sale nếu xuất hiện."""
        self.logger.info("Kiểm tra banner sale popup trên màn hình...")
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            for by, val in self.BANNER_CLOSE_LOCATORS:
                elements = self.find_elements(by, val)
                if elements and elements[0].is_displayed():
                    self.logger.info(f"Phát hiện nút đóng banner sale qua {by}={val}. Đang click 'X'...")
                    try:
                        elements[0].click()
                        time.sleep(1.0)
                        self.logger.info("Đã đóng banner sale popup thành công.")
                        return True
                    except Exception as e:
                        self.logger.warning(f"Lỗi khi click đóng banner: {e}")
            time.sleep(0.5)

        self.logger.info("Không phát hiện banner sale popup.")
        return False

    def click_live_video_tab(self, timeout: float = 10.0) -> LiveVideoPage:
        """Click vào mục xem Live & Video trên thanh tab bar."""
        self.logger.info("Tìm và click mục 'Live & Video'...")
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            for by, val in self.TAB_LIVE_VIDEO_LOCATORS:
                elements = self.find_elements(by, val)
                if elements and elements[0].is_displayed():
                    self.logger.info(f"Tìm thấy tab Live & Video qua {by}={val}. Đang click...")
                    elements[0].click()
                    return LiveVideoPage(self.driver)
            time.sleep(0.5)

        raise TimeoutError("Không tìm thấy mục 'Live & Video' trên thanh điều hướng dưới cùng!")
