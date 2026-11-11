import subprocess
from typing import List, Optional

class ADBManager:
    @staticmethod
    def get_connected_devices() -> List[str]:
        """Lấy danh sách serial các thiết bị Android đang kết nối."""
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        devices = []
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                devices.append(parts[0])
        return devices

    @staticmethod
    def take_screenshot(device_serial: Optional[str], output_path: str):
        """Chụp ảnh màn hình thiết bị thông qua adb exec-out."""
        cmd = ["adb"]
        if device_serial:
            cmd.extend(["-s", device_serial])
        cmd.extend(["exec-out", "screencap", "-p"])
        with open(output_path, "wb") as f:
            subprocess.run(cmd, stdout=f, check=True)
