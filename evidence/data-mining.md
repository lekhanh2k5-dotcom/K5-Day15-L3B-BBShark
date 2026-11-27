# Đào data — review công khai Google Play về sự cố đơn giao đồ ăn

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** review công khai trên Google Play (ngôn ngữ vi, quốc gia vn), sắp xếp mới nhất, tải ngày 27/11/2026:
  ShopeeFood (`com.deliverynow`) 10.000 review · Grab (`com.grabtaxi.passenger`), be (`xyz.be.customer`), Xanh SM (`com.gsm.customer`) mỗi app 3.000 review.
- **Đếm gì, trên tập nào, lọc gì:**
  1. `food`: review có nhắc đồ ăn / món / quán / đơn hàng (regex `FOOD` trong script).
  2. `food_issue`: trong số đó, review có nhắc một sự cố hoặc việc xử lý khiếu nại (thiếu, sai món, trễ, nguội, hoàn tiền, khiếu nại, huỷ đơn, hỗ trợ, tổng đài, chatbot…; regex `ISSUE`).
  3. `thieu_sai_mon` (đếm chặt, đúng lát cắt D1): review nói đơn bị thiếu món / sai món (regex `STRICT`).
  4. **Gán nhãn tay:** rút ngẫu nhiên 100 review trong tập `food_issue` của ShopeeFood (seed 42). Mỗi review trả lời một câu:
     *"Review này có kể chuyện đơn đồ ăn gặp sự cố mà khiếu nại không được xử lý thỏa đáng không?"* → `co` / `khong` / `khong_ro`.
     Hai người gán (Hải dòng 1–50, Khánh dòng 51–100); 10 dòng đầu cả hai cùng gán, độc lập, để đo độ khớp.
     - `co` (hoặc 1): có **cả hai** — (a) sự cố cụ thể của đơn (thiếu / sai món, trễ, đồ hỏng hoặc nguội, bị huỷ, bị trừ tiền)
       **và** (b) khiếu nại / hỗ trợ không thỏa đáng (không ai hỗ trợ, không hoàn hoặc hoàn quá lâu, bồi thường không xứng, không khiếu nại được).
     - `khong` (hoặc 2): thiếu một trong hai — chỉ kể sự cố mà không nhắc khiếu nại, hoặc nói chuyện khác (lỗi app, không cho huỷ, khuyến mãi, phí ship).
     - `khong_ro` (hoặc 3): quá mơ hồ để biết sự cố gì hoặc đã khiếu nại chưa. Phân vân giữa `co` và `khong` thì chọn `khong_ro`, ghi lý do ở `ghi_chu`.
     - Báo cáo: x = số `co`; ghi riêng số `khong_ro`, không cộng vào x.
     - **Cách gán thực tế (khai rõ):** dòng 1–10 và 51–100 do **AI gán nhãn trước** (kèm lý do ở cột `ghi_chu`),
       sau đó **Khánh đọc lại từng dòng và kiểm** (file `evidence/labels/khanh.csv`, cột `nguoi_gan` = "AI gán, Khánh kiểm").
       Dòng 1–50 do **AI gán nhãn trước** (kèm lý do ở cột `ghi_chu`), sau đó **Hải kiểm lại** (`evidence/label_sample.csv`, cột `nguoi_gan` = "AI gán, Hải kiểm").
       Dòng 1–10 có cả hai bản → độ khớp giữa hai bản trên 10 dòng chung được báo ở mục 3.
     - Soát lại lần 2 theo định nghĩa trên: sửa 3 dòng (51, 64, 88) từ `khong` thành `co` — cả 3 là "hủy đơn mà không được hoàn tiền / hoàn quá lâu".
       Lý do ghi ở cột `ghi_chu`. Số dòng Khánh sửa ở lần kiểm đầu: __ *(Khánh điền)*.
- **Mẫu số:** N = số review đã tải của từng app (không phải số người dùng app). Với kết quả gán nhãn: mẫu số = 100 review đã rút.
- **Script:** `evidence/scripts/scrape_reviews.py` → `evidence/review_counts.csv` (số đếm), `evidence/label_sample.csv` (mẫu gán nhãn).

## 2. Đọc trước, đếm sau

Đã đọc khoảng 60 review đầu của mỗi app trước khi viết bộ lọc. Các kiểu nội dung thấy được:
- Lỗi app: không đăng nhập được, không huỷ được đơn, bộ lọc khó dùng (không thuộc lát cắt).
- Đơn có sự cố: giao thiếu món, sai món, giao trễ, đồ nguội, bị huỷ đơn.
- Xử lý khiếu nại kém: chatbot vòng vo, không có tổng đài, chờ lâu, chậm hoàn tiền, bồi thường bằng voucher nhỏ.
- Chuyện tài xế, phí ship, khuyến mãi (không thuộc lát cắt).

## 3. Kết quả (đếm bằng từ khoá, chạy ngày 27/11/2026)

| App | N review | Nhắc đồ ăn/đơn | Đồ ăn + sự cố | % trên N | Thiếu / sai món (chặt) |
|---|---:|---:|---:|---:|---:|
| ShopeeFood | 10.000 | 2.587 | 779 | 7,8% | 39 |
| Grab | 3.000 | 397 | 138 | 4,6% | 10 |
| be | 3.000 | 429 | 192 | 6,4% | 9 |
| Xanh SM | 3.000 | 201 | 89 | 3,0% | 6 |
| **Cộng** | **19.000** | 3.614 | **1.198** | 6,3% | **64** |

Trong 1.198 review "đồ ăn + sự cố", 1.127 review (94%) là 1–2★.

**Gán nhãn mẫu 100 review:** **30/100** review trong mẫu đúng là "khiếu nại không được xử lý thỏa đáng" → **30%** (ngoài ra có 6/100 `khong_ro`, không cộng vào x; 64/100 `khong`). Độ khớp giữa 2 người kiểm trên 10 dòng chung (1–10): **10/10**.

## 4. ≥5 ví dụ cụ thể (nguyên văn, đã bỏ tên người viết)

1. ShopeeFood, 1★: *"qua tệ shop làm thiếu món mà yêu cầu hỗ trợ thì load mãi kh trl"*
2. ShopeeFood, 1★: *"giao sai đơn+ thiếu món là bên app hay quán giải quyết vậy.đã thanh toán qua shoppe pay r khi nào giải quyết v?!"*
3. ShopeeFood, 1★: *"Quán làm sai món rồi vứt cho khách cái vorcher 15k ko bồi hoàn dc đơn hàng phải hơm 100k app làm ăn vậy à"*
4. Grab, 1★: *"Không có tổng đài hỗ trợ cho GrabFood, gặp trục trặc không biết hỗ trợ ở đâu. Nhắn tin trên Chatbox xin hỗ trợ thì Chatb[ot]…"*
5. ShopeeFood, 2★: *"những đơn gần đây đang có tình trạng giao thiếu món, không biết vì quán giao thiếu hay tài xế lấy, nên app cần rà soát lại quy trình để kiểm tra."*
6. ShopeeFood, 1★: *"quán làm thiếu đồ nhưng shipper phải chịu hết trách nhiệm ???"* — cho thấy xử lý sai thì cả bên thứ ba cũng chịu thiệt.

## 5. Giới hạn của data

- Review cho biết người ta **gặp gì**, không cho biết **bao nhiêu người** gặp: N là số review, không phải số người dùng hay số đơn.
- Lệch tiêu cực: người gặp chuyện bực mình mới viết review → không lấy % này làm tỉ lệ sự cố của mọi đơn.
- Lọc từ khoá còn thô (vd "chậm" bắt cả app chạy chậm) → đang gán nhãn tay 100 review để đo bao nhiêu % thật sự đúng.
- Chỉ Google Play, chưa có App Store.
- → Kiểm lại bằng **phỏng vấn ≥3 người ngoài nhóm** (`evidence/interviews/`): lần gần nhất đơn có sự cố, mất bao lâu, được bồi thường gì.
