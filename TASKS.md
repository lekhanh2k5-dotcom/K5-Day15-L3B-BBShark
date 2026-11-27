# BBShark · Phân công CP2 (hạn 19:30 Thứ Sáu 27/11)

> Đề tài: **D1 · Khiếu nại đơn giao đồ ăn** (Track D). Bản đề xuất đầy đủ: xem canvas.md và spec.md.
> Làm xong phần nào thì commit + push phần đó (`git pull` trước khi push để không đè việc của nhau).
> Mỗi người chỉ sửa các file ghi trong phần của mình; cần sửa file của người khác thì nhắn nhóm trước.
> **19:00 cả nhóm ngồi lại** duyệt chuẩn "đạt" trong `spec.md` §7: chuẩn này **chốt ở CP2, sau đó không được sửa**.

## Bắt đầu

```
git clone https://github.com/lekhanh2k5-dotcom/K5-Day15-L3B-BBShark
cd K5-Day15-L3B-BBShark
python run.py          # chạy thử bản khung (AI giả), gõ vd: đơn #A101 thiếu ly trà sữa
python run.py check    # kiểm TEAMS.md + bộ câu thử
```

---

## Đoàn Công Hải · bằng chứng từ người dùng

1. **Phỏng vấn 3 bạn NGOÀI nhóm** (trong phòng C401), mỗi bạn 10–15 phút.
   - Hỏi về **lần gần nhất trong 1 tháng qua** đơn đồ ăn bị thiếu món, sai món hoặc giao trễ:
     đã làm gì · nhắn ai / qua đâu · mất bao lâu · có được bồi thường không, bao nhiêu · có thấy thỏa đáng không.
   - **Không** hỏi "bạn có muốn dùng tool này không". Không hỏi số điện thoại, địa chỉ.
   - Mỗi người một file: `evidence/interviews/P1.md`, `P2.md`, `P3.md` (chép từ `TEMPLATE.md`). **Không ghi tên.**
   - Ghi ít nhất 1 câu nói nguyên văn của mỗi người.
2. **Gán nhãn dòng 1–50** trong `evidence/label_sample.csv` (mở bằng Excel, lưu lại dạng CSV UTF-8).
   - Câu hỏi: *"Review này có kể chuyện đơn đồ ăn gặp sự cố mà khiếu nại không được xử lý thỏa đáng không?"*
   - Cột `label`: `co` · `khong` · `khong_ro`. Cột `nguoi_gan`: `Hai`. Cột `ghi_chu` tuỳ chọn.

## Hồ An Lộc · bản chạy thử và sơ đồ

1. **Đọc và chạy thử** `codebase/agent.py`, `codebase/tools.py` (đã có khung chạy được với AI giả).
   - Chạy `python run.py`, thử ít nhất 8 tin nhắn khác nhau (đơn A101–A108 trong `data/mock/orders.json`).
   - Ghi lại chỗ thấy sai hoặc thiếu vào mục "Góp ý code" cuối file này.
2. **Duyệt sơ đồ kiến trúc** trong `spec.md` §4: sơ đồ phải khớp đúng các bước trong `agent.py`.
   Chỗ nào lệch thì sửa sơ đồ hoặc báo Khánh.
3. **Viết `spec.md` §5 + §6**: ≥6 kịch bản khó (4 lớp) + 2 kịch bản tấn công, và 4 đường đi của trải nghiệm.
   Lấy ý từ các câu thử trong `eval/benchmark.csv`.

## Nguyễn Quốc Quang Anh · luồng hiện tại, giải pháp tương tự, impact

1. **`spec.md` §0 · luồng hiện tại**: mở app ShopeeFood hoặc Grab **của chính mình**, đi thử luồng báo
   "đơn thiếu món" (không cần gửi khiếu nại thật). Ghi 3–5 bước.
   Chụp màn hình, **che tên, số điện thoại, địa chỉ**, lưu vào `docs/` rồi chèn link.
2. **`spec.md` §3 · giải pháp tương tự**: trợ lý khiếu nại của Shopee / Grab / be hiện làm được gì?
   Mỗi cái: 1 điều đáng học · 1 điều đáng né · mình khác gì.
3. **`spec.md` §2 · bảng impact**: tìm số công khai **có nguồn** (link) cho: số đơn đồ ăn / tháng ở Việt Nam,
   tỉ lệ đơn có sự cố, thời gian xử lý một khiếu nại. Không có nguồn thì ghi rõ *(tự ước tính)*.
   Điền ≥3 hướng để so (D1 khiếu nại · D2 đơn nhóm · D3 trả hàng) và lý do chọn D1.
4. Đọc `data/DATA_CARD.md` và `data/mock/` (data giả), góp ý nếu data chưa giống đời thực.

## Lê Ngọc Khánh (đội trưởng) · data, câu thử, chuẩn "đạt", nộp bài

1. Data giả + `data/DATA_CARD.md` · `eval/benchmark.csv` (≥10 câu) · `eval/metric_spec.yaml`.
2. `spec.md` §1, §4 (sơ đồ), §7 (chuẩn "đạt" bản nháp để cả nhóm duyệt lúc 19:00).
3. `evidence/data-mining.md` (cách đếm review) · gán nhãn **dòng 51–100** trong `evidence/label_sample.csv`.
4. Cập nhật `canvas.md` (dòng "đã đổi gì so với CP1") · nộp form CP2.

---

## Góp ý code (Lộc ghi vào đây)

-
