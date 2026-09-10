# Tiến độ dự án IPTV

_Cập nhật: 10/09/2026 (UTC+7)_

## Mục tiêu

Tạo một URL M3U cố định cho Nm7 IPTV. Mỗi lần ứng dụng tải lại playlist, dịch vụ lấy `playlist.enc` mới nhất từ nguồn chính, giải mã và trả về danh sách M3U cập nhật.

## Nguồn và URL sử dụng

- Nguồn mã hóa: `https://raw.githubusercontent.com/hieu-TQS/ENC/main/playlist.enc`
- File M3U dự phòng trên GitHub: `https://raw.githubusercontent.com/phuongnm7/Iptv/main/SuperOK_playlist.m3u`
- URL trực tiếp dùng trong Nm7 IPTV: `https://superok-live.vercel.app/SuperOK_playlist.m3u`

Trong Nm7 IPTV, sử dụng URL Vercel ở trên. Không cần thêm tham số `?v=...`.

## Cấu hình giải mã

- Biến môi trường Vercel: `SUPEROK_TOKEN`
- Khóa giải mã: `dc5521f1fe411d6f2e83c2bf047d6294`
- Thuật toán: AES-256-CBC; khóa AES được tạo bằng SHA-256 của giá trị token, 16 byte đầu dữ liệu sau Base64 là IV.

## Phần đã hoàn thành

- Đã tạo thư mục triển khai `vercel-superok-live/`.
- Đã tạo Vercel Function tại `vercel-superok-live/api/playlist.js`.
- Function tải nguồn với chế độ không cache, giải mã AES-256-CBC và kiểm tra kết quả có định dạng M3U.
- Đã tạo rewrite `/SuperOK_playlist.m3u` sang `/api/playlist`.
- Đã thêm các header `no-store/no-cache` trong response và `vercel.json`.
- Đã triển khai project Vercel tên `superok-live`, Root Directory là `vercel-superok-live`.
- Đã cấu hình biến môi trường `SUPEROK_TOKEN` trên Vercel bằng khóa ghi tại mục Cấu hình giải mã.
- Đã xác nhận endpoint phản hồi và trình duyệt nhận nó như nội dung media/M3U. Trang chủ `/` hiện 404 là bình thường vì project không có giao diện web.
- Đã giữ workflow GitHub để đồng bộ file dự phòng `SuperOK_playlist.m3u`.

## Cơ chế cập nhật

1. Người dùng bấm tải lại/cập nhật playlist trong Nm7 IPTV.
2. Nm7 IPTV gọi URL Vercel cố định.
3. Function tải `playlist.enc` mới nhất trực tiếp từ nguồn.
4. Function giải mã và trả M3U ngay trong request.
5. Nếu nguồn chính chưa đăng bản mới, thời gian và nội dung trong playlist vẫn giữ nguyên.

Thời gian hiển thị trong nhóm `UPDATE` do nguồn chính ghi vào playlist; nó không phải thời gian cache của Vercel.

## GitHub Actions dự phòng

- `.github/workflows/sync_superok_playlist.yml`: tải, giải mã và cập nhật `SuperOK_playlist.m3u` khi nội dung nguồn thay đổi.
- `.github/workflows/superok_sync_scheduler.yml`: hỗ trợ lịch chạy đồng bộ.
- URL raw GitHub là phương án dự phòng; URL Vercel là URL chính dùng trong Nm7 IPTV.

## Các commit chính

- `44a787a330eb084830b4fba4645fbb2f43228570` — thêm gói Vercel cho endpoint SuperOK.
- `27c979ff5dc435c9d3d0fe6dcc3f5d8633e982fe` — thêm rewrite và header chống cache.
- `abc81ddc1a708711cb0fab72127fc0cecbcf29a1` — thêm endpoint giải mã trực tiếp.

## Kiểm tra khi có sự cố

- Nếu playlist chưa đổi, kiểm tra trước xem `hieu-TQS/ENC` đã cập nhật `playlist.enc` hay chưa.
- Nếu nguồn đã đổi nhưng Nm7 IPTV chưa đổi, xóa/tải lại nguồn trong ứng dụng rồi kiểm tra endpoint Vercel.
- Nếu endpoint trả lỗi 500/502, kiểm tra biến môi trường `SUPEROK_TOKEN` và Runtime Logs trên Vercel.
