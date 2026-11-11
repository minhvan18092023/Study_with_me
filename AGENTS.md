# AGENTS.md - Dự án Automation Test Android (Giai đoạn Đánh giá Song song: Appium vs Maestro vs UIAutomator2)

Tài liệu này cung cấp hướng dẫn tổng quan, mục tiêu dự án, cấu trúc môi trường song song (Appium, Maestro, UIAutomator2) và quy tắc hành xử dành cho các AI Agent (và Developer/QA) khi tham gia phát triển, bảo trì và thực thi mã nguồn trong kho lưu trữ này.

---

## 1. Tổng quan dự án (Project Overview)

- **Tên dự án:** Android Automation Testing
- **Mục đích:** Xây dựng hệ thống kiểm thử tự động (Automation Testing) toàn diện cho ứng dụng di động trên nền tảng Android.
- **Môi trường mục tiêu:**
  - **Android Real Device (Thiết bị thật):** Kết nối qua cáp USB hoặc Wi-Fi ADB. Hỗ trợ giám sát màn hình, thao tác thời gian thực thông qua `scrcpy`.
  - **Android Emulator (Máy giả lập):** Android Studio Emulator (AVD), LDPlayer, Genymotion, v.v.

---

## 2. Giai đoạn thử nghiệm song song 3 phương án (Evaluation Phase)

Hiện tại, dự án đang triển khai đồng thời **3 framework kiểm thử hàng đầu** để chạy thử nghiệm thực tế trên ứng dụng. Mục tiêu là so sánh độ ổn định, tốc độ và khả năng bảo trì trước khi chọn ra phương án chính thức (các phương án còn lại sẽ được dọn dẹp sau).

### 2.1. Phương án 1: Appium (Appium 2.x + Python Appium Client + Appium MCP Server)
- **Đặc điểm:** Tiêu chuẩn công nghiệp theo giao thức W3C WebDriver, độc lập ngôn ngữ, khả năng mở rộng đa nền tảng (Android & iOS).
- **Ưu điểm:** Hệ sinh thái lớn, tài liệu phong phú, hỗ trợ tốt đa dạng locator (Accessibility ID, XPath, UIAutomator selector), dễ tích hợp CI/CD. Đã tích hợp **Appium MCP Server chính chủ (`appium-mcp`)** phục vụ AI Agent tự động hóa.
- **Nhược điểm:** Cần cài đặt Appium Server + Driver, tốc độ thực thi tương đối chậm hơn so với giao tiếp trực tiếp.
- **Thư mục quản lý:** `frameworks/appium/`

### 2.2. Phương án 2: Maestro (mobile.dev)
- **Đặc điểm:** Framework thế hệ mới định dạng declarative (YAML-based), tập trung vào sự đơn giản và độ tin cậy. Đầy đủ bộ công cụ CLI mạnh mẽ tương tự Playwright (`maestro studio`, `maestro test`).
- **Ưu điểm:** Viết kịch bản cực kỳ nhanh, cú pháp trực quan, cơ chế tự động chờ (built-in resilience, chống flaky test tốt), không cần code boilerplate. `maestro studio` hỗ trợ inspect giao diện thời gian thực qua web browser tương tự Playwright Codegen.
- **Nhược điểm:** Xử lý logic rẽ nhánh phức tạp (conditional branching) cần dùng JavaScript nhúng, cấu trúc kịch bản thiên về YAML thay vì code OOP truyền thống.
- **Thư mục quản lý:** `frameworks/maestro/`

### 2.3. Phương án 3: UIAutomator2 (Python `uiautomator2`)
- **Đặc điểm:** Thư viện Python giao tiếp trực tiếp với Android UIAutomator thông qua RPC daemon chạy trên thiết bị.
- **Ưu điểm:** Siêu nhẹ, tốc độ thực thi cực nhanh, tương tác sâu với hệ thống Android (ADB, app info, notification, wifi, screen unlock,...), viết code Python thuần kết hợp `pytest`.
- **Nhược điểm:** Chỉ dành riêng cho Android, phụ thuộc daemon cài trên máy khách/thiết bị.
- **Lưu ý bảo mật MCP:** Không sử dụng các MCP server trôi nổi của bên thứ 3 cho UIAutomator2 (không có bản chính chủ từ OpenATX). Mọi thao tác UIAutomator2 được thực hiện trực tiếp qua Python script/Pytest.
- **Thư mục quản lý:** `frameworks/uiautomator2/`

---

## 3. Tiêu chí đánh giá lựa chọn chính thức (Evaluation Criteria)

| Tiêu chí | Trọng số | Mô tả đánh giá |
| :--- | :---: | :--- |
| **Độ ổn định (Stability / Low Flakiness)** | 35% | Ít bị lỗi vặt do timeout, render trễ, nhảy màn hình |
| **Tốc độ thực thi (Execution Speed)** | 25% | Thời gian khởi động session và hoàn thành test flow |
| **Tương tác thiết bị & Scrcpy (Hardware Integration)** | 20% | Độ mượt mà khi kết hợp cùng ADB, scrcpy, cắm/rút thiết bị thật |
| **Dễ bảo trì & Phát triển (Maintainability & Dev Experience)** | 20% | Tốc độ viết test mới, debug khi fail, tính dễ đọc của code |

> [!NOTE]
> Khi đã xác định được framework tối ưu nhất trong thực tế, AI Agent hoặc team sẽ cập nhật lại `AGENTS.md` thành framework duy nhất và lưu trữ/dọn dẹp mã nguồn của 2 framework còn lại.

---

## 4. Cấu trúc thư mục dự án (Project Structure)

```text
├── configs/                  # Cấu hình thiết bị (capabilities, serial, app package)
│   ├── devices.yaml          # Thông tin thiết bị thật / giả lập
│   └── app_config.yaml       # Thông tin package, activity, timeout
├── drivers/                  # Quản lý kết nối ADB và Scrcpy
│   ├── adb_manager.py        # Helper quản lý thiết bị ADB, bắt logcat, screenshot
│   └── scrcpy_manager.py     # Điều khiển hiển thị màn hình qua Scrcpy
├── frameworks/               # 3 framework đang được đánh giá song song
│   ├── appium/
│   │   ├── conftest.py       # Fixture pytest cho Appium session
│   │   ├── pages/            # Page Object Model cho Appium
│   │   └── tests/            # Test cases viết bằng Appium
│   ├── maestro/
│   │   ├── config.yaml       # Cấu hình Maestro
│   │   ├── flows/            # Kịch bản kiểm thử dạng YAML
│   │   └── subflows/         # Các flow tái sử dụng (Login, Navigation,...)
│   └── uiautomator2/
│       ├── conftest.py       # Fixture pytest cho uiautomator2
│       ├── pages/            # Page Object Model cho uiautomator2
│       └── tests/            # Test cases viết bằng uiautomator2
├── reports/                  # Thư mục chứa báo cáo (Allure, HTML, logs, videos)
├── utils/                    # Các module dùng chung (logger, data generator)
├── requirements.txt          # Danh sách thư viện Python
└── AGENTS.md                 # Hướng dẫn dành cho AI Agents
```

---

## 5. Hướng dẫn & Quy tắc dành cho AI Agent (Agent Guidelines)

### 5.1. Quy trình bắt buộc khi khởi tạo phiên làm việc (Session Initialization & Device Handling)
1. **Xác nhận môi trường thực thi (Thiết bị thật vs Giả lập):**
   - Khi bắt đầu một phiên làm việc/kiểm thử mới mà người dùng chưa nêu rõ môi trường, **AI Agent phải chủ động hỏi người dùng**:
     - *Bạn muốn chạy phiên kiểm thử trên **Thiết bị thật (Real Device)** kết nối qua ADB hay **Máy giả lập (Emulator)**?*
2. **Kiểm tra kết nối ADB:**
   ```bash
   adb devices
   ```
   - Nếu không thấy thiết bị hoặc trạng thái `unauthorized`/`offline`, hướng dẫn người dùng bật USB Debugging hoặc chấp nhận quyền trên điện thoại.
3. **Tự động khởi động `scrcpy` đối với Thiết bị thật qua ADB:**
   - **Bắt buộc:** Nếu phiên chạy trên **Thiết bị thật qua Android ADB**, AI Agent phải **tự động khởi động tiến trình `scrcpy`** để đưa màn hình điện thoại hiển thị trực tiếp lên màn hình máy tính (`scrcpy -s <device_serial> --max-size 1024`).
   - Kiểm tra xem `scrcpy` đã chạy cho thiết bị đó chưa (`pgrep -f "scrcpy.*<device_serial>"`), nếu chưa thì khởi động ở chế độ background.
   - Điều này giúp người dùng quan sát trực quan mọi thao tác kiểm thử thời gian thực mà không cần nhìn vào màn hình điện thoại cầm tay.
4. **Chỉ định Target Device:**
   Khi có nhiều thiết bị/emulator cùng cắm, luôn luôn dùng cờ `-s <device_serial>` trong các lệnh ADB, cấu hình `udid` trong Appium/Maestro/UIAutomator2.
5. **Môi trường thực thi từng framework:**
   - **Appium:** Đảm bảo Appium Server đang chạy: `appium -p 4723`.
   - **Maestro:** Đảm bảo `maestro` CLI đã cài đặt trong PATH (`export PATH="$PATH:$HOME/.maestro/bin"`).
   - **UIAutomator2:** Đảm bảo thiết bị đã khởi tạo uiautomator daemon (`python3 -m uiautomator2 init` nếu cần).

### 5.2. Quy trình bắt buộc khi phát triển kịch bản kiểm thử (Inspect-Before-Code Workflow)
**Nguyên tắc cốt lõi:** Khi cần thực hiện bất kỳ kịch bản kiểm thử nào, **tuyệt đối không phỏng đoán locator hay viết code/flow ngay khi chưa xác thực giao diện thực tế**. AI Agent và QA phải tuân thủ nghiêm ngặt quy trình 3 bước:

1. **Bước 1: Khảo sát màn hình thực tế (Screen Survey):**
   - Đưa ứng dụng tới màn hình cần kiểm thử trên thiết bị thật / máy giả lập.
   - Quan sát trực quan trạng thái màn hình (thông qua cửa sổ `scrcpy` đã bật hoặc chụp ảnh màn hình qua ADB).

2. **Bước 2: Tìm và xác thực chính xác Locator:**
   - **Với Maestro:** Khởi chạy `maestro studio` (truy cập `http://localhost:9999`) để click trực tiếp vào view, lấy selector tối ưu hoặc dùng `maestro hierarchy` xuất cây giao diện.
   - **Với Appium:** Dùng `appium-mcp` (hoặc Appium Inspector) để inspect page source và xác định element attributes.
   - **Với UIAutomator2:** Dump UI hierarchy hoặc truy vấn selector trực tiếp qua Python.
   - **Thứ tự ưu tiên locator:** `resource-id` duy nhất > `accessibility-id` (content-desc) > `text` đặc trưng > `XPath` tương đối ngắn (tuyệt đối không dùng absolute XPath dài dễ vỡ).

3. **Bước 3: Viết mã kiểm thử và cấu trúc hóa:**
   - **Cập nhật Page Object trước:** Đưa toàn bộ locator và hàm thao tác vào `pages/` (cho Appium / UIAutomator2), không viết cứng locator trong test script.
   - **Với Maestro:** Viết hoặc bổ sung subflows/flows dạng YAML dựa trên selector đã kiểm chứng.
   - **Explicit Waits over Hard Sleeps:** Tuyệt đối tránh `time.sleep()` dài cố định. Sử dụng cơ chế wait thông minh (Auto-wait của Maestro, WebDriverWait của Appium, `wait()` của UIAutomator2).
   - **Failure Artifacts:** Luôn bắt buộc ghi logcat và chụp ảnh màn hình khi có test case thất bại.

### 5.3. Hướng dẫn chọn công cụ & Khi nào dùng cái gì (Tool Usage Matrix)

| Công cụ / Phương thức | Khi nào nên sử dụng? | Mục đích & Lợi thế |
| :--- | :--- | :--- |
| **`maestro studio`** | **Khi khảo sát màn hình mới, tìm locator hoặc debug kịch bản** | Hoạt động như *Playwright Codegen / Inspector*: Mở Web UI trực quan, click thẳng vào view để lấy selector tối ưu (text, id), chạy thử các lệnh tương tác tức thì và copy cú pháp YAML mà không cần mò XML. |
| **`maestro test <flow.yaml>`** | **Khi chạy tự động hóa flow đã viết hoàn chỉnh hoặc chạy theo lô (batch)** | Chạy kịch bản kiểm thử không cần can thiệp người dùng. Có sẵn cơ chế tự động chờ (Auto-Wait), chống flaky khi ứng dụng tải chậm, xuất kết quả trực tiếp ra console/CI. |
| **`appium-mcp` (Appium MCP Server)** | **Khi AI Agent cần tự hành tương tác thiết bị qua Appium** | Cung cấp giao thức Model Context Protocol chuẩn W3C cho AI Agent kết nối Appium Server, cho phép AI tự query elements, tap, swipe hoặc chạy logic test linh hoạt mà không cần viết test script cố định từ trước. |
| **Appium Pytest (`frameworks/appium/`)** | **Khi chạy test case Appium theo mô hình OOP / POM chuẩn** | Dành cho các bộ test hồi quy phức tạp, cần quản lý dữ liệu lớn, fixture pytest và sinh báo cáo HTML/Allure chuyên nghiệp. |
| **UIAutomator2 Pytest (`frameworks/uiautomator2/`)** | **Khi cần tốc độ thực thi siêu nhanh hoặc can thiệp sâu hệ thống Android** | Tương tác trực tiếp qua RPC daemon: tắt/bật Wi-Fi, bắt notification, chạy lệnh ADB, mở Notification panel, mở app cực nhanh. **Không dùng MCP server bên thứ 3** để đảm bảo an toàn tuyệt đối. |

### 5.4. Quản lý tài nguyên và an toàn
- **Dọn dẹp sau khi chạy:** Đóng tiến trình `scrcpy` khi phiên làm việc kết thúc (hoặc khi người dùng yêu cầu đóng), dừng Appium session hoặc giải phóng kết nối RPC sau khi hoàn tất test.
- **An toàn thiết bị:** Không tự ý thực thi các lệnh phá hủy như `wipe data`, reset máy nếu không có chỉ thị rõ ràng.
- **An toàn MCP Server:** Chỉ sử dụng MCP Server chính chủ (`appium-mcp` từ Appium Foundation). Tuyệt đối không cài đặt hoặc chạy các MCP server không rõ nguồn gốc từ bên thứ ba.

---

## 6. Lệnh thường dùng cho từng Framework (Quick References)

### ADB & Scrcpy:
```bash
# Kiểm tra thiết bị
adb devices

# Kết nối scrcpy quan sát màn hình
scrcpy -s <device_serial> --max-size 1024

# Chụp ảnh màn hình trực tiếp từ ADB
adb -s <device_serial> exec-out screencap -p > screenshot.png
```

### 1. Appium & Appium MCP:
```bash
# Khởi động Appium server (port mặc định 4723)
appium --port 4723

# Khởi động Appium MCP Server (cho AI Agent tương tác trực tiếp)
appium-mcp

# Chạy test suite Appium với pytest
pytest frameworks/appium/tests/ --html=reports/appium_report.html
```

### 2. Maestro:
```bash
# 1. Khảo sát / Inspect / Debug UI (tương đương Playwright Codegen/Inspector)
maestro studio
# (Mở trình duyệt tại http://localhost:9999 để chọn element, sinh lệnh)

# 2. Thực thi kiểm thử tự động một flow cụ thể
maestro --device <device_serial> test frameworks/maestro/flows/sample_flow.yaml

# 3. Chạy toàn bộ thư mục test flows
maestro test frameworks/maestro/flows/

# 4. Xuất cây phân cấp giao diện ra terminal
maestro hierarchy
```

### 3. UIAutomator2:
```bash
# Khởi tạo thiết bị cho uiautomator2
python3 -m uiautomator2 init

# Chạy test suite uiautomator2 với pytest
pytest frameworks/uiautomator2/tests/ --html=reports/u2_report.html
```
