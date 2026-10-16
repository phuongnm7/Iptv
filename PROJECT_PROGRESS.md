# Tiến độ hệ thống playlist NM7 IPTV

_Cập nhật: 16/10/2026 (UTC+7)_

## URL công khai đang dùng

- **Nguồn mặc định cho NM7 IPTV Mobile, NM7 IPTV TV và NM7 IPTV iOS:** `https://phuongnm7-playlist.phuongnm7-iptv.workers.dev/`
- **Nguồn dự phòng / gộp playlist cho NM7 TV Web:** `https://iptv-live-merge.phuongnm7-iptv.workers.dev/playlist.m3u`
- **Playlist thể thao:** `https://thethaonm7.phuongnm7-iptv.workers.dev/playlist.m3u`

Các URL Worker công khai được giữ nguyên để không cần phát hành lại app chỉ vì thay đổi tài khoản GitHub.

## Nguồn dữ liệu hiện tại

- Danh mục truyền hình tự cập nhật: `https://raw.githubusercontent.com/dungntk9/Iptv-phuongnm7/main/generated/vapptv-live.m3u`
- Sự kiện FPT PLAY: `https://raw.githubusercontent.com/dungntk9/Iptv-phuongnm7/main/IPTV_Gop_VMTTV_vAppTV.m3u` (lọc nhóm sự kiện)
- Playlist thể thao cập nhật: `https://raw.githubusercontent.com/dungntk9/Iptv-phuongnm7/main/sports-auto.m3u`
- Danh sách VIP: `https://raw.githubusercontent.com/dungntk9/Iptv-phuongnm7/main/VIP-307.m3u`

`SuperOK_playlist.m3u` được giữ nguyên làm bản dự phòng 425 kênh. Nó không còn là nguồn trực tiếp của playlist mặc định và workflow tạo playlist đã bỏ việc tải qua `superok-live.vercel.app`.

## Lịch cập nhật

- Danh mục vAppTV: workflow được cấu hình chạy mỗi 10 phút.
- Playlist thể thao và playlist chọn lọc: workflow được cấu hình chạy mỗi 5 phút.
- Worker mặc định đọc các nguồn GitHub công khai khi có yêu cầu và tắt cache HTTP cho phản hồi M3U.
- Lịch 5 phút được giữ nguyên.

## Thay đổi đã commit

- Sửa bộ lọc nhóm kênh để khớp với các nhóm thật trong nguồn playlist hiện hành.
- Thay nguồn thể thao TinyURL đang trả HTTP 404 bằng file `sports-auto.m3u` trong repo mới.
- Thay nguồn cũ gắn với Vercel bằng danh mục tự cập nhật thuộc repo `dungntk9/Iptv-phuongnm7`.
- Giữ thứ tự nhóm truyền hình chính ở đầu playlist.
- Cập nhật nguồn cho NM7 TV Web stable để không gọi endpoint VietMiTV trên Vercel.

## Trạng thái triển khai

Mã nguồn và workflow kiểm tra đã được commit. Trạng thái **production chưa được xác nhận** cho đến khi workflow triển khai Worker chạy thành công và vượt qua smoke test endpoint công khai:

- Deploy cả hai playlist Worker: `https://github.com/dungntk9/Iptv-phuongnm7/actions/workflows/deploy-nm7-default-playlist-cutover.yml`
- Deploy riêng Worker mặc định: `https://github.com/dungntk9/Iptv/actions/workflows/deploy-default-playlist-worker.yml`
- Deploy NM7 TV Web stable: `https://github.com/dungntk9/nm7-tv-web/actions/workflows/cloudflare-deploy.yml`

Nếu workflow báo thiếu secret, repo cần có `CLOUDFLARE_API_TOKEN` và `CLOUDFLARE_ACCOUNT_ID` trong Actions secrets.
