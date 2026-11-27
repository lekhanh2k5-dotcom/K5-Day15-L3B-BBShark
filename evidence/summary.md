# Tổng hợp bằng chứng pain

> Bản CP3 (cập nhật 27/11 tối). Nguồn chính: **đào review công khai** (đạt ngưỡng). Phỏng vấn và khảo sát đang làm, sẽ bổ sung trước khi nộp CP3.
> Giả thuyết ban đầu: `evidence/hypothesis.md` (giả thuyết gốc ghi ở canvas CP1, commit `2c8e118`, 16:46 27/11).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data: review công khai Google Play (x/N, %, cách đếm ghi trước, script chạy lại được, ≥5 ví dụ) | ☑ Đạt | `evidence/data-mining.md` · `evidence/review_stats.md` · `evidence/scripts/` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ Đang làm (0/3) | `evidence/interviews/` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ Đang làm (form đã soạn) | `evidence/survey/` |

## 2. Số chính

- **Đào data** (19.000 review Google Play mới nhất của ShopeeFood, Grab, be, Xanh SM; đăng 01/2025 → 26/11/2026; tải 27/11/2026):
  - **1.198/19.000 (6,3%)** review nhắc sự cố đơn đồ ăn hoặc việc xử lý khiếu nại; **1.127/1.198 (94%)** trong số đó là 1–2★.
  - Chủ đề trong 1.198 review có sự cố (đếm từ khoá, một review có thể thuộc nhiều nhóm): huỷ đơn 587 (49%) · **hỗ trợ / CSKH / chatbot kém 326 (27%)** · giao trễ 318 (27%) · **hoàn tiền chậm / không hoàn 207 (17%)** · đồ hỏng, nguội 124 (10%) · **thiếu / sai món 52 (4%)**.
  - Cùng khoảng 15/09 → 26/11/2026: tỉ lệ review có sự cố ShopeeFood 73/951 (7,7%) · be 31/483 (6,4%) · Grab 93/1.681 (5,5%) · Xanh SM 89/3.000 (3,0%).
  - **Gán nhãn tay** mẫu 100 review ngẫu nhiên (seed 42) trong tập có sự cố của ShopeeFood: đã xong 60/100. Dòng 51–100: **17/50 review là "khiếu nại không được xử lý thỏa đáng"**, 4/50 không rõ *(dòng 1–10 và 51–100: AI gán, Khánh kiểm từng dòng; dòng 1–50 Hải gán tay — đang làm)*. Kết quả trên đủ 100 dòng và độ khớp giữa hai người: cập nhật trước CP3.
- **Phỏng vấn:** chưa có (đang hẹn).
- **Khảo sát:** chưa có (form 11 câu, gửi tối 27/11).

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "qua tệ shop làm thiếu món mà yêu cầu hỗ trợ thì load mãi kh trl" — review ShopeeFood, 1★
2. "giao sai đơn+ thiếu món là bên app hay quán giải quyết vậy.đã thanh toán qua shoppe pay r khi nào giải quyết v?!" — review ShopeeFood, 1★
3. "Quán làm sai món rồi vứt cho khách cái vorcher 15k ko bồi hoàn dc đơn hàng phải hơm 100k app làm ăn vậy à" — review ShopeeFood, 1★
4. "Không có tổng đài hỗ trợ cho GrabFood, gặp trục trặc không biết hỗ trợ ở đâu. Nhắn tin trên Chatbox xin hỗ trợ thì Chatb[ot]…" — review Grab, 1★
5. "những đơn gần đây đang có tình trạng giao thiếu món, không biết vì quán giao thiếu hay tài xế lấy, nên app cần rà soát lại quy trình để kiểm tra." — review ShopeeFood, 2★
6. "quán làm thiếu đồ nhưng shipper phải chịu hết trách nhiệm ???" — review ShopeeFood, 1★ (xử lý sai thì bên thứ ba chịu thiệt)
7. Quan sát trực tiếp app ShopeeFood (27/11/2026, tài khoản Quang Anh): trợ lý "Tép Thám Tử" dặn "nhập nội dung chat ngắn gọn, có dấu, không viết tắt", nhận ý "giao sai/thiếu món" rồi đẩy về nút "Chọn đơn hàng" / hướng dẫn gửi ảnh — `spec.md` §0, ảnh `docs/shopeefood-huong-ho-tro.jpg`.

## 4. Các nguồn có khớp nhau không

Hiện mới có **một nguồn đạt ngưỡng** (review), cộng một quan sát trực tiếp trên app. Review nói: khi đơn gặp sự cố, phần người dùng bực nhất là **xử lý khiếu nại** (hỗ trợ kém 27%, hoàn tiền chậm 17%), không chỉ bản thân sự cố. Quan sát app khớp một phần: trợ lý đã nhận chat nhưng vẫn đẩy về form. **Chưa kiểm chéo với người dùng** — phỏng vấn và khảo sát sẽ trả lời: lần gần nhất mất bao lâu, kết quả gì, có dùng trợ lý tự động không.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` ("khiếu nại đơn đồ ăn thường không được xử lý nhanh và đúng mức"): **đúng một phần, phải đổi cách nói** — review cho thấy nỗi đau nằm ở khâu xử lý khiếu nại (hỗ trợ, hoàn tiền), còn thiếu / sai món chỉ chiếm 4% review có sự cố. Nhóm giữ lát cắt thiếu / sai món / giao trễ làm ca demo vì luật bồi thường rõ và kiểm được bằng code; đơn bị huỷ (49%) bị loại vì phụ thuộc cổng thanh toán (`spec.md` §2).
Điều vẫn chưa biết: tỉ lệ người dùng thật gặp sự cố mỗi tháng, thời gian chờ thực tế, và trợ lý tự động có giúp được không — chờ khảo sát và phỏng vấn.

## Lịch hẹn (chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên đặt đồ ăn qua app (ngoài nhóm) | *(Hải điền)* | |
