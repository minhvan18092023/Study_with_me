import os
import subprocess
import time
import pytest
import requests
import yaml
from appium import webdriver
from appium.options.android import UiAutomator2Options
from drivers.adb_manager import ADBManager
from drivers.scrcpy_manager import ScrcpyManager
from utils.logger import get_logger

logger = get_logger("Appium_Conftest")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "../../configs/config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def ensure_appium_server(host="127.0.0.1", port=4723):
    url = f"http://{host}:{port}/status"
    try:
        res = requests.get(url, timeout=2)
        if res.status_code == 200:
            logger.info("Appium server đã đang chạy sẵn.")
            return None
    except Exception:
        pass

    logger.info(f"Khởi động Appium server tự động trên cổng {port}...")
    proc = subprocess.Popen(
        ["appium", "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    for _ in range(15):
        time.sleep(1)
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                logger.info(f"Appium server đã sẵn sàng (PID: {proc.pid}).")
                return proc
        except Exception:
            continue
    logger.warning("Không thể khởi động Appium server tự động!")
    return proc

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
def setup_environment(device_serial):
    """Đảm bảo Appium server và Scrcpy đều đang hoạt động."""
    ScrcpyManager.start(device_serial)
    server_proc = ensure_appium_server()
    yield
    if server_proc:
        server_proc.terminate()

@pytest.fixture(scope="function")
def appium_driver(device_serial):
    config = load_config()
    app_cfg = config.get("app", {})

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = device_serial
    options.device_name = device_serial
    options.app_package = app_cfg.get("package_name", "com.shopee.vn")
    options.app_activity = app_cfg.get("main_activity", "com.shopee.app.ui.home.HomeActivity_")
    options.app_wait_activity = app_cfg.get("app_wait_activity", "*")
    options.no_reset = True
    options.set_capability("newCommandTimeout", 120)
    options.set_capability("autoGrantPermissions", True)

    server_url = "http://127.0.0.1:4723"
    logger.info(f"Đang tạo phiên Appium tới {server_url} với UDID: {device_serial}...")
    driver = webdriver.Remote(command_executor=server_url, options=options)
    driver.implicitly_wait(config.get("timeouts", {}).get("implicit_wait", 10))

    yield driver

    logger.info("Đóng phiên Appium Driver...")
    try:
        driver.quit()
    except Exception:
        pass
