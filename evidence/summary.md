# Tổng hợp bằng chứng pain

> Bản CP3 (cập nhật 28/11 sáng). Nguồn chính: **đào review công khai** (đạt ngưỡng). Khảo sát: 20 phản hồi (28/11). Phỏng vấn: 3 người (27/11).
> Giả thuyết ban đầu: `evidence/hypothesis.md` (giả thuyết gốc ghi ở canvas CP1, commit `2c8e118`, 16:46 27/11).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data: review công khai Google Play (x/N, %, cách đếm ghi trước, script chạy lại được, ≥5 ví dụ) | ☑ Đạt | `evidence/data-mining.md` · `evidence/review_stats.md` · `evidence/scripts/` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ Đạt: 3/3 người, 2/3 kể được một lần khiếu nại bị xử lý chậm hoặc không thỏa đáng trong 1 tháng qua | `evidence/interviews/P1.md` · `P2.md` · `P3.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ Đủ 20 phản hồi, gửi qua Discord riêng tư + Zalo *(form không có câu xác nhận người ngoài nhóm)* | `evidence/survey/questions.md` · `evidence/survey/results.csv` · `evidence/scripts/survey_stats.py` |

## 2. Số chính

- **Đào data** (19.000 review Google Play mới nhất của ShopeeFood, Grab, be, Xanh SM; đăng 01/2025 → 26/11/2026; tải 27/11/2026):
  - **1.198/19.000 (6,3%)** review nhắc sự cố đơn đồ ăn hoặc việc xử lý khiếu nại; **1.127/1.198 (94%)** trong số đó là 1–2★.
  - Chủ đề trong 1.198 review có sự cố (đếm từ khoá, một review có thể thuộc nhiều nhóm): huỷ đơn 587 (49%) · **hỗ trợ / CSKH / chatbot kém 326 (27%)** · giao trễ 318 (27%) · **hoàn tiền chậm / không hoàn 207 (17%)** · đồ hỏng, nguội 124 (10%) · **thiếu / sai món 52 (4%)**.
  - Cùng khoảng 15/09 → 26/11/2026: tỉ lệ review có sự cố ShopeeFood 73/951 (7,7%) · be 31/483 (6,4%) · Grab 93/1.681 (5,5%) · Xanh SM 89/3.000 (3,0%).
  - **Gán nhãn mẫu 100 review** ngẫu nhiên (seed 42) trong tập có sự cố của ShopeeFood: đã xong **100/100**. Kết quả chung: **30/100 (30%)** review là "khiếu nại không được xử lý thỏa đáng", 6/100 `khong_ro`, 64/100 `khong` *(dòng 1–50: AI gán, Hải kiểm — 13 `co`, 35 `khong`, 2 `khong_ro`; dòng 51–100: AI gán, Khánh kiểm — 17 `co`, 29 `khong`, 4 `khong_ro`)*. Độ khớp trên 10 dòng chung (1–10): **10/10**.
- **Khảo sát** (form 11 câu, Discord riêng tư + Zalo, 20 phản hồi lúc 03:02–03:28 ngày 28/11; bản điền thử tối 27/11 đã loại; đếm bằng `python evidence/scripts/survey_stats.py`, theo ngưỡng ở `evidence/hypothesis.md`):
  - **16/20 (80%)** gặp trục trặc với đơn đồ ăn trong 3 tháng qua (12/20 trong 1 tháng qua) → **đạt** ngưỡng ≥ 1/3.
  - **13/18** người từng gặp có báo sự cố. Trong 13 người đó, **6/13 (46%)** chờ từ 1 giờ trở lên hoặc chỉ nhận xin lỗi / bị từ chối / chưa có kết quả → **chưa đạt** ngưỡng ≥ 1/2.
  - 11/13 người báo có dùng trợ lý tự động trong app. Trong 11 người này: **7/11 phải chờ chuyển sang nhân viên**, 6/11 phải bấm qua nhiều nút hoặc điền form, 3/11 trợ lý không hiểu và phải gõ lại, 3/11 trợ lý hiểu đúng ngay.
  - Điểm hài lòng (13 người đã báo): 1★ 1 · 2★ 3 · 3★ 3 · 4★ 4 · 5★ 2. Thiếu / sai món là trục trặc nặng nhất với 6/20 người.
  - Giới hạn: form không hỏi người điền có ở ngoài nhóm không; chỉ 4/20 người viết câu 11.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | học viên L3B | Một phần: thiếu món, được hoàn đúng 15.000đ nhưng chờ khoảng 3 tiếng | 1 | khoảng 3 tiếng | chụp ảnh hoá đơn, gửi form qua bot trong app |
| P2 | học viên L3B | Có: sai mức đường + giao trễ, bị từ chối hoàn tiền, chỉ nhận voucher 15.000đ (đơn 55.000đ) | 2 | 30–40 phút | nhắn tài xế, rồi chờ nối chat nhân viên vì bot không có đúng mục lỗi |
| P3 | học viên L3B | Một phần: đồ ăn bị đổ, được huỷ đơn không mất tiền (COD) | 1 | khoảng 25 phút | đặt COD với món có nước, kiểm túi trước mặt shipper |

Phỏng vấn ngày 27/11/2026, TV4 hỏi và ghi. Ngưỡng ở `hypothesis.md`: ≥ 2/3 người kể được một lần như thế trong 1 tháng qua. Tiêu chí "như thế" dùng giống khảo sát: chờ từ 1 giờ trở lên, hoặc chỉ xin lỗi / bị từ chối / chưa có kết quả. P1 (chờ khoảng 3 tiếng) và P2 (bị từ chối hoàn tiền) đạt; P3 (25 phút, được huỷ đơn) không → **2/3, đạt**.

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "qua tệ shop làm thiếu món mà yêu cầu hỗ trợ thì load mãi kh trl" — review ShopeeFood, 1★
2. "giao sai đơn+ thiếu món là bên app hay quán giải quyết vậy.đã thanh toán qua shoppe pay r khi nào giải quyết v?!" — review ShopeeFood, 1★
3. "Quán làm sai món rồi vứt cho khách cái vorcher 15k ko bồi hoàn dc đơn hàng phải hơm 100k app làm ăn vậy à" — review ShopeeFood, 1★
4. "Không có tổng đài hỗ trợ cho GrabFood, gặp trục trặc không biết hỗ trợ ở đâu. Nhắn tin trên Chatbox xin hỗ trợ thì Chatb[ot]…" — review Grab, 1★
5. "những đơn gần đây đang có tình trạng giao thiếu món, không biết vì quán giao thiếu hay tài xế lấy, nên app cần rà soát lại quy trình để kiểm tra." — review ShopeeFood, 2★
6. "quán làm thiếu đồ nhưng shipper phải chịu hết trách nhiệm ???" — review ShopeeFood, 1★ (xử lý sai thì bên thứ ba chịu thiệt)
7. "nhắn qua chatbot mấy vòng mới gặp được nhân viên, rồi chờ hơn 2 ngày tiền mới hoàn về ví." — khảo sát, GrabFood, bị trừ tiền 2 lần, 3★
8. "phải gọi qua gọi lại giữa tài xế và nhân viên hỗ trợ để chụp hóa đơn chứng minh không phải lỗi do mình lấy nhầm." — khảo sát, ShopeeFood, sai món, 4★
9. "mất hơn nửa ngày chờ hỗ trợ mới chốt hoàn tiền." — khảo sát, GrabFood, đồ ăn bị đổ, 2★
10. Quan sát trực tiếp app ShopeeFood (27/11/2026, tài khoản Quang Anh): trợ lý "Tép Thám Tử" dặn "nhập nội dung chat ngắn gọn, có dấu, không viết tắt", nhận ý "giao sai/thiếu món" rồi đẩy về nút "Chọn đơn hàng" / hướng dẫn gửi ảnh — `spec.md` §0, ảnh `docs/shopeefood-huong-ho-tro.jpg`.

## 4. Các nguồn có khớp nhau không

Review nói: khi đơn gặp sự cố, phần người dùng bực nhất là **xử lý khiếu nại** (hỗ trợ kém 27%, hoàn tiền chậm 17%), không chỉ bản thân sự cố. Quan sát app khớp một phần: trợ lý đã nhận chat nhưng vẫn đẩy về form.
Khảo sát **khớp ở khâu trợ lý**: 7/11 người dùng trợ lý phải chờ chuyển sang nhân viên, 6/11 phải bấm nút hoặc điền form, giống điều quan sát trên app. Khảo sát **lệch ở mức độ**: chỉ 6/13 người báo sự cố chờ từ 1 giờ trở lên hoặc không được giải quyết, và 6/13 chấm 4–5★. Tức là nhiều ca vẫn được xử lý ổn, đúng với "cách giải thích khác" đã ghi trong `hypothesis.md`.
Phỏng vấn **khớp với khảo sát ở khâu trợ lý**: P1 thấy các bước bấm của bot rối, phải tìm kỹ chỗ đính ảnh; P2 không tìm thấy mục lỗi phù hợp nên phải chờ nối nhân viên. Điểm **mới**: cả 3 người đều tự chụp ảnh làm bằng chứng và bỏ qua bước gọi quán; P1 nói tiền hoàn sau 3 tiếng "không cứu được bữa ăn"; P2 định không báo các lỗi nhẹ nữa; P3 cố ý chọn COD để dễ xử lý tại chỗ.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` ("khiếu nại đơn đồ ăn thường không được xử lý nhanh và đúng mức"): **đúng một phần, phải đổi cách nói** — review cho thấy nỗi đau nằm ở khâu xử lý khiếu nại (hỗ trợ, hoàn tiền), còn thiếu / sai món chỉ chiếm 4% review có sự cố. Nhóm giữ lát cắt thiếu / sai món / giao trễ làm ca demo vì luật bồi thường rõ và kiểm được bằng code; đơn bị huỷ (49%) bị loại vì phụ thuộc cổng thanh toán (`spec.md` §2).
Khảo sát (n = 20) cho thấy trục trặc xảy ra thường xuyên (16/20 người trong 3 tháng qua) và trợ lý tự động hay phải chuyển sang nhân viên (7/11). Nhưng ngưỡng "≥ 1/2 người báo bị xử lý chậm hoặc không thỏa đáng" **chưa đạt** (6/13), nên nỗi đau rõ nhất nằm ở **khâu trợ lý vòng vèo, phải chờ người**, hơn là ở việc không được bồi thường. Phỏng vấn (3 người, đạt ngưỡng 2/3) cũng cho thấy vướng chính là bot thiếu mục lỗi và phải chờ, còn khi được xử lý thì thường là hoàn đúng tiền món. Thêm một điều nhóm chưa nghĩ tới: với người dùng, tốc độ xử lý quan trọng ngang số tiền được hoàn, vì bữa ăn đã lỡ.

## Lịch hẹn (chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| P1 · học viên L3B đặt đồ ăn qua app (ngoài nhóm) | 27/11 18:14 | ☑ |
| P2 · học viên L3B đặt đồ ăn qua app (ngoài nhóm) | 27/11 18:32 | ☑ |
| P3 · học viên L3B đặt đồ ăn qua app (ngoài nhóm) | 27/11 18:50 | ☑ |
