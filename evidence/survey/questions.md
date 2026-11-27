# Khảo sát — bộ câu hỏi, kênh gửi, thời gian

- **Công cụ:** Google Forms (Hải tạo; câu hỏi do nhóm soạn, Claude Code rà, xem `docs/ai-usage.md`).
- **Kênh gửi:** Discord riêng tư + Zalo. 
- **Mở / chốt:** câu trả lời đầu tiên lúc 03:02, cuối cùng lúc 03:28 ngày 28/11/2026; xuất file lúc 03:30.
- **Bản điền thử bị loại:** 20 dòng điền lúc 18:03–18:56 ngày 27/11 bị loại và xoá khỏi form, vì câu 11 là câu mẫu có đánh số và câu trả lời trái với logic chuyển phần. Các dòng này không có trong `results.csv`.
- **Không thu** tên, email, SĐT. Form **không có câu** xác nhận người điền ở ngoài nhóm (giới hạn, xem `evidence/summary.md`).
- **Kết quả:** `results.csv` (20 dòng, chỉ giữ ngày, bỏ giờ điền). Đếm bằng `python evidence/scripts/survey_stats.py`.

## Câu hỏi (giữ nguyên câu)

Các lựa chọn dưới đây chép từ bản xuất. Lựa chọn nào chưa có ai chọn thì Hải bổ sung từ form.

| # | Câu hỏi | Kiểu · lựa chọn |
|---|---|---|
| 1 | Trung bình mỗi tháng bạn đặt đồ ăn qua app bao nhiêu lần? | Chọn một: Dưới 1 lần · 1–3 lần · 4–10 lần · Hơn 10 lần |
| 2 | Lần gần nhất đơn đồ ăn của bạn gặp trục trặc (thiếu món, sai món, giao trễ, đồ hỏng hoặc đổ, đơn bị huỷ, bị trừ tiền sai) là cách đây bao lâu? | Chọn một: Trong 1 tuần · 1–4 tuần · 1–3 tháng · Hơn 3 tháng · Chưa từng gặp (→ kết thúc) |
| 3 | Lần đó bạn đặt qua app nào? | Chọn một: ShopeeFood · GrabFood · beFood · Xanh SM · Khác |
| 4 | Trục trặc nào ảnh hưởng đến bạn nhiều nhất? | Chọn một: Thiếu món · Sai món · Giao trễ · Đồ ăn hỏng, đổ hoặc kém chất lượng · Đơn bị huỷ · Bị trừ tiền sai · Khác |
| 5 | Sau đó bạn có báo sự cố (khiếu nại) không? | Chọn một: Có · Không (→ chuyển phần) |
| 6 | Bạn đã báo bằng cách nào? | Chọn nhiều: Trợ lý tự động / chat bot trong app · Chat với nhân viên hỗ trợ · Gọi tổng đài · Liên hệ quán hoặc tài xế · Viết đánh giá hoặc đăng mạng xã hội · Khác |
| 7 | Nếu đã nhắn trợ lý tự động trong app, bạn gặp những gì? | Chọn nhiều: Trợ lý hiểu đúng ngay · Phải bấm qua nhiều nút hoặc điền form · Trợ lý không hiểu, phải gõ lại · Phải chờ chuyển sang nhân viên · Tôi không dùng trợ lý tự động |
| 8 | Từ lúc báo đến khi có kết quả cuối cùng mất bao lâu? | Chọn một: Dưới 10 phút · 10 đến dưới 60 phút · 1 đến 24 giờ · Trên 24 giờ · Đến giờ chưa có |
| 9 | Kết quả bạn nhận được là gì? | Chọn nhiều: Hoàn toàn bộ tiền · Hoàn một phần · Voucher · Giao lại hoặc giao bù · Chỉ xin lỗi · Bị từ chối · Chưa có kết quả · Khác |
| 10 | Bạn hài lòng thế nào với cách sự cố được giải quyết? | Thang 1–5 |
| 11 | Kể ngắn gọn chuyện đã xảy ra. Điều gì khó chịu nhất? Nếu bạn không báo sự cố, vì sao? | Đoạn văn, không bắt buộc |
