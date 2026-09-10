# Tiến độ dự án IPTV

_Cập nhật: 10/09/2026 (UTC+7)_

## URL sử dụng

- File M3U dự phòng: `https://raw.githubusercontent.com/phuongnm7/Iptv/main/SuperOK_playlist.m3u`
- URL chính dùng trong Nm7 IPTV: `https://superok-live.vercel.app/SuperOK_playlist.m3u`

## Cấu trúc dự án

- Repo `phuongnm7/Iptv` tiếp tục chứa các playlist M3U công khai.
- Mã Vercel và cấu hình giải mã đã chuyển sang repo riêng tư `phuongnm7/superok-live-private`.
- Khóa giải mã không còn được ghi trên nhánh `main` hiện tại của repo công khai.

## Cơ chế cập nhật

1. Nm7 IPTV gọi URL Vercel khi người dùng tải lại playlist.
2. Vercel tải file nguồn mới nhất.
3. Function trong repo riêng tư giải mã và trả M3U ngay trong request.
4. Nếu nguồn chính chưa cập nhật, thời gian và nội dung playlist vẫn giữ nguyên.

Thời gian trong nhóm `UPDATE` do nguồn chính ghi vào playlist, không phải thời gian cache của Vercel.

## Trạng thái

- Endpoint Vercel đã triển khai và hoạt động.
- Trang chủ `/` trả 404 là bình thường vì project chỉ cung cấp API/M3U.
- Mã triển khai không còn nằm trên nhánh hiện tại của repo công khai.
- Các playlist `Iptv.m3u`, `Iptv1.m3u`, `SPORT.m3u` và `SuperOK_playlist.m3u` vẫn được giữ nguyên.
