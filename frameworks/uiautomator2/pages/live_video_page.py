import time
import uiautomator2 as u2
from .base_page import BasePage

class LiveVideoPage(BasePage):
    """Màn hình Live & Video Shopee."""

    # Dấu hiệu nhận biết đang ở màn hình Live & Video
    INDICATOR_SELECTORS = [
        {"description": "click video comment_icon"},
        {"description": "like vide"},
        {"description": "click video share icon"},
        {"textMatches": r".*(LIVE|Live|Mua ngay|Xem sản phẩm|Thêm bình luận|Chia sẻ|Vuốt lên để xem thêm).*"},
        {"descriptionMatches": r".*(video|live|buynow|comment|share).*"},
    ]

    def is_displayed(self, timeout: float = 10.0) -> bool:
        """Kiểm tra màn hình Live & Video có đang hiển thị nội dung video hay không."""
        self.logger.info("Xác thực màn hình Live & Video đang hiển thị...")
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            for sel_kwargs in self.INDICATOR_SELECTORS:
                el = self.d(**sel_kwargs)
                if el.exists:
                    self.logger.info(f"Đã xác nhận vào màn hình Live & Video thành công (tìm thấy: {sel_kwargs}).")
                    return True
            time.sleep(0.5)

        self.logger.warning("Không tìm thấy dấu hiệu nhận biết của màn hình Live & Video trong thời gian quy định.")
        return False
