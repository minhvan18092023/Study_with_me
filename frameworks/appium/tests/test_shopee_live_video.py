import os
import pytest
from frameworks.appium.pages.home_page import HomePage
from utils.logger import get_logger

logger = get_logger("TestShopeeLiveVideo_Appium")

class TestShopeeLiveVideoAppium:
    """
    Kịch bản kiểm thử (Appium):
    1. Mở ứng dụng Shopee.
    2. Nếu xuất hiện banner sale / popup quảng cáo thì click 'X' để đóng.
    3. Click vào mục xem 'Live & Video'.
    4. Xác minh màn hình Live & Video hiển thị thành công.
    """

    def test_open_shopee_close_banner_and_view_live(self, appium_driver):
        logger.info("=== BẮT ĐẦU TEST CASE (Appium): Mở Shopee -> Đóng Banner nếu có -> Vào Live & Video ===")
        home_page = HomePage(appium_driver)

        # Bước 1: Kiểm tra và đóng banner sale nếu xuất hiện
        closed = home_page.dismiss_sale_banner_if_present(timeout=4.0)
        if closed:
            logger.info("Đã phát hiện và đóng banner sale popup thành công.")
        else:
            logger.info("Không có banner sale popup xuất hiện, tiếp tục kịch bản.")

        # Bước 2: Click vào mục xem Live & Video
        live_video_page = home_page.click_live_video_tab(timeout=10.0)

        # Bước 3: Xác minh giao diện Live & Video đã hiển thị
        assert live_video_page.is_displayed(timeout=10.0), "Màn hình Live & Video không hiển thị thành công!"
        
        # Chụp ảnh báo cáo
        os.makedirs("reports/screenshots", exist_ok=True)
        live_video_page.take_screenshot("reports/screenshots/appium_live_video_success.png")
        logger.info("=== KẾT THÚC TEST CASE APPIUM THÀNH CÔNG ===")
