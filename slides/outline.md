# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | 64 review nhắc thiếu/sai món. Dùng trích dẫn ShopeeFood số 1 trong evidence/data-mining.md và ảnh hướng hỗ trợ ở spec.md §0. | `evidence/summary.md` | ☐ |
| 2 | Vì sao chọn bài này | Cùng 100 người gặp việc mỗi tháng: D1 1.250 phút, D2 2.000, D3 1.500 (tự ước tính). Chọn D1 vì đã có bằng chứng và đơn để kiểm đáp án. | `spec.md` §2 | ☐ |
| 3 | Giải pháp | Khách báo món thiếu → tra đơn → tính giá món bằng code → đề xuất. Quá 200.000đ thì chuyển người theo chính sách dựng. | `spec.md` §4 | ☐ |
| 4 | Demo live | B01: thiếu 1 trà sữa, kỳ vọng đề xuất 35.000đ. B10: phần thiếu 203.000đ, kỳ vọng chuyển người. Khi demo đối chiếu output thật với hai đáp án. | `eval/benchmark.csv` | ☐ |
| 5 | **Đánh giá thế nào** | 27 câu, 9 từ review, 4 metric. Bổ sung run ID, kết quả hai lượt và lỗi chính khi có file đã chấm. | `eval/README.md`, `eval/report.md` | ☐ |
| 6 | **Chi phí khi dùng thật** | 50 phiên dự kiến. Ba quy mô 50/100/200 khách (tự ước tính). Bổ sung chi phí/task thành công từ token thật và tỉ lệ đạt. | `cost/cost-estimate.md` | ☐ |
| 7 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6 | — | ☐ |
| 8 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | ☐ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| | |
