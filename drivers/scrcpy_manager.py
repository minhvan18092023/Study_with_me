import subprocess
import shutil
from typing import Optional

class ScrcpyManager:
    """Quản lý tiến trình scrcpy để hiển thị màn hình thiết bị Android lên máy tính."""

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("scrcpy") is not None

    @staticmethod
    def is_running(device_serial: Optional[str] = None) -> bool:
        """Kiểm tra xem scrcpy có đang chạy cho device_serial cụ thể không."""
        try:
            import os
            current_pid = str(os.getpid())
            cmd = ["pgrep", "-f", f"^scrcpy.*{device_serial}" if device_serial else "^scrcpy"]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                # Thử fallback tìm process nhị phân scrcpy
                res = subprocess.run(["pgrep", "-x", "scrcpy"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                pids = [p.strip() for p in res.stdout.split() if p.strip() and p.strip() != current_pid]
                return len(pids) > 0
            pids = [p.strip() for p in result.stdout.split() if p.strip() and p.strip() != current_pid]
            return len(pids) > 0
        except Exception:
            return False

    @staticmethod
    def start(device_serial: Optional[str] = None, max_size: int = 1024, window_title: Optional[str] = None) -> Optional[subprocess.Popen]:
        """
        Khởi động scrcpy dưới nền (background).
        Tự động bỏ qua nếu scrcpy cho thiết bị này đã chạy sẵn.
        """
        if not ScrcpyManager.is_installed():
            print("[ScrcpyManager] Cảnh báo: 'scrcpy' chưa được cài đặt trên máy.")
            return None

        if ScrcpyManager.is_running(device_serial):
            print(f"[ScrcpyManager] scrcpy cho thiết bị {device_serial or 'mặc định'} đã đang chạy.")
            return None

        cmd = ["scrcpy"]
        if device_serial:
            cmd.extend(["-s", device_serial])
        if max_size:
            cmd.extend(["--max-size", str(max_size)])
        
        title = window_title or (f"Android Device ({device_serial})" if device_serial else "Android Device")
        cmd.extend(["--window-title", title])

        # Chạy ngầm, không block terminal/test runner
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        print(f"[ScrcpyManager] Đã khởi động scrcpy cho thiết bị {device_serial or 'mặc định'} (PID: {process.pid}).")
        return process

    @staticmethod
    def stop(device_serial: Optional[str] = None):
        """Dừng tiến trình scrcpy."""
        pattern = f"scrcpy.*{device_serial}" if device_serial else "scrcpy"
        subprocess.run(["pkill", "-f", pattern], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[ScrcpyManager] Đã dừng scrcpy ({pattern}).")
