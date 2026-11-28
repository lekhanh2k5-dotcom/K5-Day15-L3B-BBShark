# Tổng hợp bằng chứng pain

> Bản CP3 (cập nhật 28/11 sáng). Nguồn chính: **đào review công khai** (đạt ngưỡng). Nguồn thứ hai: **phỏng vấn 3 người** (27/11, đạt ngưỡng).
> Giả thuyết ban đầu: `evidence/hypothesis.md` (giả thuyết gốc ghi ở canvas CP1, commit `2c8e118`, 16:46 27/11).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data: review công khai Google Play (x/N, %, cách đếm ghi trước, script chạy lại được, ≥5 ví dụ) | ☑ Đạt | `evidence/data-mining.md` · `evidence/review_stats.md` · `evidence/scripts/` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ Đạt: 3/3 người, 2/3 kể được một lần khiếu nại bị xử lý chậm hoặc không thỏa đáng trong 1 tháng qua | `evidence/interviews/P1.md` · `P2.md` · `P3.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ Không dùng ở bản này | — |

## 2. Số chính

- **Đào data** (19.000 review Google Play mới nhất của ShopeeFood, Grab, be, Xanh SM; đăng 01/2025 → 26/11/2026; tải 27/11/2026):
  - **1.198/19.000 (6,3%)** review nhắc sự cố đơn đồ ăn hoặc việc xử lý khiếu nại; **1.127/1.198 (94%)** trong số đó là 1–2★.
  - Chủ đề trong 1.198 review có sự cố (đếm từ khoá, một review có thể thuộc nhiều nhóm): huỷ đơn 587 (49%) · **hỗ trợ / CSKH / chatbot kém 326 (27%)** · giao trễ 318 (27%) · **hoàn tiền chậm / không hoàn 207 (17%)** · đồ hỏng, nguội 124 (10%) · **thiếu / sai món 52 (4%)**.
  - Cùng khoảng 15/09 → 26/11/2026: tỉ lệ review có sự cố ShopeeFood 73/951 (7,7%) · be 31/483 (6,4%) · Grab 93/1.681 (5,5%) · Xanh SM 89/3.000 (3,0%).
  - **Gán nhãn mẫu 100 review** ngẫu nhiên (seed 42) trong tập có sự cố của ShopeeFood: đã xong **100/100**. Kết quả chung: **30/100 (30%)** review là "khiếu nại không được xử lý thỏa đáng", 6/100 `khong_ro`, 64/100 `khong` *(dòng 1–50: AI gán, Hải kiểm — 13 `co`, 35 `khong`, 2 `khong_ro`; dòng 51–100: AI gán, Khánh kiểm — 17 `co`, 29 `khong`, 4 `khong_ro`)*. Trên 10 dòng chung (1–10) hai bản cho cùng nhãn **10/10** — lưu ý cả hai bản đều do AI gán trước rồi người kiểm, nên đây **không phải** độ khớp giữa hai người gán độc lập.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | học viên L3B | Một phần: thiếu món, được hoàn đúng 15.000đ nhưng chờ khoảng 3 tiếng | 1 | khoảng 3 tiếng | chụp ảnh hoá đơn, gửi form qua bot trong app |
| P2 | học viên L3B | Có: sai mức đường + giao trễ, bị từ chối hoàn tiền, chỉ nhận voucher 15.000đ (đơn 55.000đ) | 2 | 30–40 phút | nhắn tài xế, rồi chờ nối chat nhân viên vì bot không có đúng mục lỗi |
| P3 | học viên L3B | Một phần: đồ ăn bị đổ, được huỷ đơn không mất tiền (COD) | 1 | khoảng 25 phút | đặt COD với món có nước, kiểm túi trước mặt shipper |

Phỏng vấn ngày 27/11/2026, TV4 hỏi và ghi. Ngưỡng ở `hypothesis.md`: ≥ 2/3 người kể được một lần như thế trong 1 tháng qua. Tiêu chí "như thế" (ghi ở `hypothesis.md`): chờ từ 1 giờ trở lên, hoặc chỉ xin lỗi / bị từ chối / chưa có kết quả. P1 (chờ khoảng 3 tiếng) và P2 (bị từ chối hoàn tiền) đạt; P3 (25 phút, được huỷ đơn) không → **2/3, đạt**.

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "qua tệ shop làm thiếu món mà yêu cầu hỗ trợ thì load mãi kh trl" — review ShopeeFood, 1★
2. "giao sai đơn+ thiếu món là bên app hay quán giải quyết vậy.đã thanh toán qua shoppe pay r khi nào giải quyết v?!" — review ShopeeFood, 1★
3. "Quán làm sai món rồi vứt cho khách cái vorcher 15k ko bồi hoàn dc đơn hàng phải hơm 100k app làm ăn vậy à" — review ShopeeFood, 1★
4. "Không có tổng đài hỗ trợ cho GrabFood, gặp trục trặc không biết hỗ trợ ở đâu. Nhắn tin trên Chatbox xin hỗ trợ thì Chatb[ot]…" — review Grab, 1★
5. "những đơn gần đây đang có tình trạng giao thiếu món, không biết vì quán giao thiếu hay tài xế lấy, nên app cần rà soát lại quy trình để kiểm tra." — review ShopeeFood, 2★
6. "quán làm thiếu đồ nhưng shipper phải chịu hết trách nhiệm ???" — review ShopeeFood, 1★ (xử lý sai thì bên thứ ba chịu thiệt)
7. "hoàn 15 ngàn sau đó 3 tiếng cũng đâu có biến thành tô canh ngay lúc ăn được." — phỏng vấn P1 (thiếu món, chờ khoảng 3 tiếng)
8. "Mình ngồi giải thích với nhân viên hỗ trợ cả buổi, chụp rõ cái tem 100% đường gửi qua luôn mà cuối cùng app chốt cho cái voucher 15 ngàn ép đặt đơn sau, ly trà sữa 55 ngàn coi như đổ bỏ." — phỏng vấn P2
9. "đứng ngoài cổng giải quyết gần nửa tiếng rồi đặt lại quán khác, thành ra gần 9 giờ tối mới có cơm ăn." — phỏng vấn P3
10. Quan sát trực tiếp app ShopeeFood (27/11/2026, tài khoản Quang Anh): trợ lý "Tép Thám Tử" dặn "nhập nội dung chat ngắn gọn, có dấu, không viết tắt", nhận ý "giao sai/thiếu món" rồi đẩy về nút "Chọn đơn hàng" / hướng dẫn gửi ảnh — `spec.md` §0, ảnh `docs/shopeefood-huong-ho-tro.jpg`.

## 4. Các nguồn có khớp nhau không

Review nói: khi đơn gặp sự cố, phần người dùng bực nhất là **xử lý khiếu nại** (hỗ trợ kém 27%, hoàn tiền chậm 17%), không chỉ bản thân sự cố. Quan sát app khớp một phần: trợ lý đã nhận chat nhưng vẫn đẩy về form.
Phỏng vấn **khớp với review và quan sát app ở khâu trợ lý**: P1 thấy các bước bấm của bot rối, phải tìm kỹ chỗ đính ảnh; P2 không tìm thấy mục lỗi phù hợp nên phải chờ nối nhân viên. Điểm **mới**: cả 3 người đều tự chụp ảnh làm bằng chứng và bỏ qua bước gọi quán; P1 nói tiền hoàn sau 3 tiếng "không cứu được bữa ăn"; P2 định không báo các lỗi nhẹ nữa; P3 cố ý chọn COD để dễ xử lý tại chỗ.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` ("khiếu nại đơn đồ ăn thường không được xử lý nhanh và đúng mức"): **đúng một phần, phải đổi cách nói** — review cho thấy nỗi đau nằm ở khâu xử lý khiếu nại (hỗ trợ, hoàn tiền), còn thiếu / sai món chỉ chiếm 4% review có sự cố. Nhóm giữ lát cắt thiếu / sai món / giao trễ làm ca demo vì luật bồi thường rõ và kiểm được bằng code; đơn bị huỷ (49%) bị loại vì phụ thuộc cổng thanh toán (`spec.md` §2).
Phỏng vấn (3 người, đạt ngưỡng 2/3) cũng cho thấy vướng chính là bot thiếu mục lỗi và phải chờ, còn khi được xử lý thì thường là hoàn đúng tiền món. Thêm một điều nhóm chưa nghĩ tới: với người dùng, tốc độ xử lý quan trọng ngang số tiền được hoàn, vì bữa ăn đã lỡ.

## Lịch hẹn (chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| P1 · học viên L3B đặt đồ ăn qua app (ngoài nhóm) | 27/11 18:14 | ☑ |
| P2 · học viên L3B đặt đồ ăn qua app (ngoài nhóm) | 27/11 18:32 | ☑ |
| P3 · học viên L3B đặt đồ ăn qua app (ngoài nhóm) | 27/11 18:50 | ☑ |
