import time
import uiautomator2 as u2
from .base_page import BasePage
from .live_video_page import LiveVideoPage

class HomePage(BasePage):
    """Trang chủ ứng dụng Shopee."""

    # Selectors cho nút đóng Banner Sale / Quảng cáo
    BANNER_CLOSE_SELECTORS = [
        {"resourceIdMatches": r".*(btn_close|button_close|close_btn|iv_close|dialog_close).*"},
        {"descriptionMatches": r"(?i).*(đóng|close|dismiss|cancel).*"},
        {"textMatches": r"(?i)^(✕|✖|X|x|Đóng|Close)$"},
        {"resourceId": "com.shopee.vn:id/button_close"},
    ]

    # Selectors cho tab Live & Video
    TAB_LIVE_VIDEO_SELECTORS = [
        {"description": "tab_bar_button_video_and_live"},
        {"text": "Live & Video"},
        {"textMatches": r".*Live & Video.*"},
    ]

    def dismiss_sale_banner_if_present(self, timeout: float = 4.0) -> bool:
        """
        Kiểm tra nếu xuất hiện banner sale / quảng cáo dạng popup, click nút 'X' để đóng.
        Trả về True nếu có đóng banner, False nếu không xuất hiện.
        """
        self.logger.info("Kiểm tra sự xuất hiện của banner sale/quảng cáo...")
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            for sel_kwargs in self.BANNER_CLOSE_SELECTORS:
                el = self.d(**sel_kwargs)
                if el.exists:
                    self.logger.info(f"Phát hiện nút đóng banner sale qua selector {sel_kwargs}. Đang click 'X'...")
                    try:
                        el.click()
                        time.sleep(1.0)
                        self.logger.info("Đã click đóng banner sale thành công.")
                        return True
                    except Exception as e:
                        self.logger.warning(f"Lỗi khi click nút đóng banner: {e}")
            time.sleep(0.5)

        self.logger.info("Không phát hiện banner sale hoặc banner đã tự đóng.")
        return False

    def click_live_video_tab(self, timeout: float = 10.0) -> LiveVideoPage:
        """
        Click vào mục 'Live & Video' trên thanh điều hướng dưới cùng.
        """
        self.logger.info("Tìm và click vào mục 'Live & Video'...")
        end_time = time.time() + timeout
        clicked = False

        while time.time() < end_time:
            for sel_kwargs in self.TAB_LIVE_VIDEO_SELECTORS:
                el = self.d(**sel_kwargs)
                if el.exists:
                    self.logger.info(f"Tìm thấy tab Live & Video bằng {sel_kwargs}. Thực hiện click...")
                    el.click()
                    clicked = True
                    break
            if clicked:
                break
            time.sleep(0.5)

        if not clicked:
            raise TimeoutError("Không tìm thấy mục 'Live & Video' trên thanh điều hướng dưới cùng!")

        return LiveVideoPage(self.d)
