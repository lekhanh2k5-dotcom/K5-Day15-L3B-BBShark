# Data card — dữ liệu bản chạy thử dùng (bản đầu CP2)

> Data trong `data/mock/` là **synthetic** (nhóm tự dựng) → dùng để chạy thử và làm câu thử, **không phải bằng chứng pain**.
> Bằng chứng pain lấy từ review công khai: xem `evidence/data-mining.md`.

## Dataset 1 · Đơn hàng giả (`data/mock/orders.json`)

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `get_order`, `compute_remedy` · căn cứ đáp án của `eval/benchmark.csv` |
| Từ đâu | nhóm tự dựng: 8 đơn viết tay (A101–A108, mỗi đơn phục vụ một nhóm câu thử) + 22 đơn sinh ngẫu nhiên |
| Xử lý những bước gì | sinh bằng `data/make_mock_data.py`, seed 15, chạy lại ra đúng cùng file |
| Số dòng | 30 đơn, 4 quán dựng ("Quán Mẫu …"), khách K01–K30 |
| Phiên bản / ngày | mock-2026-11-27 |
| Nhãn | `synthetic` |
| Giới hạn | giá và món đặt theo mức phổ biến ở TP.HCM do nhóm ước lượng; không có đơn nhiều quán, không có topping; giờ giao chỉ là số phút so với giờ hẹn |

## Dataset 2 · Chính sách bồi thường dựng (`data/mock/policy.json`)

| | |
|---|---|
| Dùng để làm gì | nguồn cho `get_policy`, `check_limit`; quy tắc chấm `khong_vuot_han_muc` |
| Từ đâu | nhóm tự viết, tham khảo cách trình bày ở trang trợ giúp công khai của các app giao đồ ăn; **không phải chính sách của hãng nào** |
| Nội dung | thiếu món / sai món: hoàn giá món theo đơn, tự xử lý tối đa 200.000đ · trễ quá 30 phút: voucher 50.000đ · chuyển người khi vượt mức, ≥3 khiếu nại/30 ngày, nghi ngộ độc / dị ứng, khách đòi gặp nhân viên |
| Nhãn | `synthetic` |
| Nguồn từng luật | trễ quá 30 phút → voucher 50.000đ: theo ví dụ "chính sách dựng" trong đề Track D (tình huống khó của D1) · hoàn đúng giá món thiếu / sai, vượt hạn mức thì chuyển người, ngộ độc / dị ứng / dị vật thì chuyển người ngay, không đưa số điện thoại: theo phần tình huống khó và An toàn của đề Track D · **hạn mức tự xử lý 200.000đ và ngưỡng ≥3 khiếu nại / 30 ngày (viết cứng trong `codebase/agent.py`): nhóm tự đặt *(tự ước tính)***. Đối chiếu thực tế: ShopeeFood yêu cầu ảnh đơn thực nhận để xem xét bồi hoàn, điều khoản Grab có liệt kê thiếu món trong các trường hợp được hoàn (`spec.md` §3); không hãng nào công bố hạn mức bằng số |
| Giới hạn | ngưỡng 200.000đ, 30 phút, 50.000đ là số dựng để thử; chưa có luật cho đơn bị huỷ, hoàn phí ship |

## Dataset 3 · Lịch sử khiếu nại giả (`data/mock/complaints.json`)

| | |
|---|---|
| Dùng để làm gì | nguồn cho `get_complaint_history` (một căn cứ để chuyển người, không dùng để từ chối) |
| Từ đâu | sinh bằng `data/make_mock_data.py`, seed 15 |
| Số dòng | 9 khiếu nại; khách K05 có 5 lần trong tháng 11 để thử ca "khiếu nại nhiều lần" |
| Nhãn | `synthetic` |

## Dataset 4 · Review công khai Google Play (bằng chứng, không dùng cho bản chạy thử)

| | |
|---|---|
| Dùng để làm gì | đào bằng chứng pain · lấy câu nói nguyên văn cho 6 câu thử `data_that` |
| Từ đâu | review công khai trên Google Play: ShopeeFood, Grab, be, Xanh SM; tải ngày 27/11/2026 bằng `evidence/scripts/scrape_reviews.py` |
| Xử lý | lọc từ khoá 2 bước (đồ ăn/đơn → sự cố); bỏ tên người viết, ảnh, mã người dùng; mã review băm 10 ký tự |
| Số dòng | 19.000 review (ShopeeFood 10.000 mới nhất, mỗi app khác 3.000); số đếm ở `evidence/review_counts.csv` |
| Nhãn | thật (công khai) · file đầy đủ `evidence/raw-reviews.csv` **không commit** |
| Giới hạn | người bực mình hay viết review hơn → lệch về phía tiêu cực, không đại diện cho mọi người dùng; lọc từ khoá còn thô (đang gán nhãn tay 100 review để đo độ chính xác) |
