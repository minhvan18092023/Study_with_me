import os
import time
import pytest
import yaml
import uiautomator2 as u2
from drivers.adb_manager import ADBManager
from drivers.scrcpy_manager import ScrcpyManager
from utils.logger import get_logger

logger = get_logger("UIAutomator2_Conftest")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "../../configs/config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

@pytest.fixture(scope="session")
def device_serial():
    config = load_config()
    serial = config.get("target_device", {}).get("serial")
    if not serial:
        devices = ADBManager.get_connected_devices()
        if not devices:
            pytest.skip("Không có thiết bị Android nào kết nối qua ADB!")
        serial = devices[0]
    return serial

@pytest.fixture(scope="session", autouse=True)
def setup_scrcpy(device_serial):
    """Đảm bảo scrcpy đang chạy để phản chiếu màn hình thiết bị."""
    logger.info(f"Khởi động scrcpy cho thiết bị {device_serial}...")
    ScrcpyManager.start(device_serial)
    yield
    # Không bắt buộc dừng scrcpy để tiện cho người dùng tiếp tục quan sát

@pytest.fixture(scope="function")
def u2_device(device_serial):
    """Khởi tạo session UIAutomator2 và mở ứng dụng Shopee."""
    logger.info(f"Kết nối tới thiết bị qua uiautomator2: {device_serial}")
    d = u2.connect(device_serial)
    
    package_name = "com.shopee.vn"
    logger.info(f"Khởi động ứng dụng {package_name}...")
    d.app_stop(package_name)
    time.sleep(1)
    d.app_start(package_name)
    time.sleep(3) # Cho ứng dụng thời gian load Splash Screen
    
    yield d

    logger.info("Kết thúc test case UIAutomator2.")
