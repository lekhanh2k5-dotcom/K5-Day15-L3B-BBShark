# BBShark · Phân công CP4 (hạn 14:30 Thứ Bảy 28/11)

> CP3 đã nộp. CP4 là bản dùng để **xét giải** (cùng phần demo).
> Vẫn KHÔNG sửa: `spec.md` §7, `eval/metric_spec.yaml`, đáp án (`expected`) câu thử cũ, `data/mock/`, `eval/run-1.csv`, `traces/run-1.jsonl`.
> Lượt 2 chỉ sửa **hệ thống** (prompt, code), chạy **trọn 27 câu**. Không bỏ câu trượt, không chạy lại nhiều lần để chọn kết quả đẹp.
> Sửa `codebase/` xong → `python eval/check_decisions.py` phải ra 0 câu trượt.
> Mỗi việc: nhánh mới từ `main` → commit → push → pull request. Khánh merge.

**CP4 cần:** lượt 1 → lượt 2 · chi phí / task thành công + 3 kịch bản (kèm tên model) · `spec.md` đủ §0–§9 · `demo-slides.pdf` ở thư mục gốc + link video demo dự phòng · phần chưa xong.

## Lịch

| Giờ | Việc |
|---|---|
| 09:30 | Khánh xong sửa prompt `sai_mon` + `cost/personas.yaml` |
| 10:00–10:30 | Lộc chạy lượt 2 + simulate 50 phiên |
| 10:30–12:00 | Khánh viết báo cáo đánh giá, chi phí và mời người dùng thử · Quang Anh làm slide nháp · Hải tìm số liệu chi phí |
| 12:00–13:30 | Hoàn thiện slide, xuất PDF · Lộc quay video dự phòng |
| 13:30–14:15 | Cả nhóm tập demo 2 phút, ai cũng nói được 1 phần |
| 14:30 | Khánh nộp CP4 |

## Hồ An Lộc · lượt 2, chi phí, video dự phòng

1. Sau khi PR sửa prompt `sai_mon` được merge: `git pull`, rồi `python run.py eval` → `eval/run-2.csv` + `traces/run-2.jsonl` → `python eval/grade.py eval/run-2.csv` → `python run.py score eval/run-2.csv`. Commit cả hai file. Cùng model với lượt 1 (`gpt-4o-mini`).
2. Sau khi `cost/personas.yaml` được sửa: `python run.py simulate` (≥50 phiên, model thật) → `cost/simulate-N.csv` + `cost/simulate-N-summary.md`. Commit.
3. Quay **video demo dự phòng** (1–2 phút): 1 trường hợp thường + 1 trường hợp khó (vd tấn công chèn lệnh, hoặc khiếu nại vượt hạn mức → chuyển nhân viên). Drive "Bất kỳ ai có đường liên kết". Gửi link cho Khánh.
4. Điền các ô ghi "khai" của mình trong `docs/ai-usage.md`.
5. Hạn: lượt 2 + simulate trước 10:30; video trước 13:30.

## Nguyễn Quốc Quang Anh · slide

1. **Slide 8 trang** theo guide 5.1, mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo. Mẫu: `slides/outline.md`.
   1) Người dùng & nỗi đau (Hải soạn nội dung) · 2) Vì sao chọn bài (bảng impact `spec.md` §2) · 3) Giải pháp (lát cắt, sơ đồ `docs/ai-architecture.svg`, AI tự làm đến đâu) · 4) Demo live · 5) Đánh giá (lượt 1 → lượt 2, lấy từ `eval/README.md`) · 6) Chi phí (lấy từ `cost/cost-estimate.md`) · 7) Kết luận go / iterate / stop · 8) Nếu có thêm 1 tuần.
   Xuất **`demo-slides.pdf` ở thư mục gốc repo**.
2. Điền các ô ghi "khai" của mình trong `docs/ai-usage.md`.
3. Hạn: slide nháp 12:00, PDF 13:30.

## Đoàn Công Hải · số liệu chi phí, slide trang 1

1. **Số liệu quy mô thật cho phần chi phí** → file mới `cost/scale-sources.md`, nộp PR trước 11:00.
   - **Để làm gì:** `python run.py simulate` chỉ cho biết chi phí **một** lần xử lý khiếu nại. Phần chi phí (R6, 12 điểm) phải phóng lên **quy mô thật** theo 3 kịch bản thấp · cơ sở · cao. Đề yêu cầu track D lấy quy mô từ **số người dùng của sản phẩm, nguồn công khai có link** (không dùng số 700 học viên của khoá).
   - **Công thức Khánh sẽ dùng:**
     `Số khiếu nại / tháng = số đơn đồ ăn / tháng × tỉ lệ đơn có sự cố × tỉ lệ người có báo sự cố`
     `Chi phí / tháng = số khiếu nại / tháng × chi phí / task thành công (từ simulate)`
   - **Cần tìm:**

     | Số liệu | Đã có | Gợi ý nguồn |
     |---|---|---|
     | Số đơn đồ ăn qua app / tháng ở Việt Nam | Ken Research ≈ 29,2 triệu đơn/tháng (`spec.md` §2) — tìm **thêm 1 nguồn** để đối chiếu | Momentum Works, Statista, Q&Me, Decision Lab, báo chí (VnExpress, CafeF, Tuổi Trẻ) |
     | Số người dùng / thị phần từng app (ShopeeFood, GrabFood, be, Xanh SM) | chưa | Báo cáo thị trường, báo chí, công bố của hãng — dùng để dựng kịch bản "chỉ một app" (thấp) và "cả thị trường" (cao) |
     | Tỉ lệ đơn có sự cố (thiếu / sai món, trễ, hỏng) | chưa | Báo cáo, khảo sát công khai; hiếm có — không có thì ghi *(tự ước tính)* |
     | Tỉ lệ người gặp sự cố có báo / khiếu nại | chưa | Như trên. Có thể tham khảo phỏng vấn P1–P3 (n = 3, chỉ tham khảo) |

   - **Cách ghi trong `cost/scale-sources.md`** — một bảng, mỗi dòng một số liệu:
     `Số liệu | Giá trị | Năm / kỳ của số liệu | Link nguồn | Ngày xem | Ghi chú (cách tính, nếu tự quy đổi)`
     Sau bảng, đề xuất giá trị cho 3 kịch bản (thấp · cơ sở · cao) kèm 1 dòng lý do mỗi kịch bản.
   - **Luật:** mỗi số phải có link + ngày xem, hoặc ghi rõ *(tự ước tính)* kèm lý do. Không lấy số từ trang không mở được, không lấy từ đoạn trích của công cụ tìm kiếm. Quy đổi (vd năm → tháng) thì ghi cách tính.
2. Soạn **nội dung slide trang 1** (người dùng & nỗi đau) gửi Quang Anh: số review, kết quả nhãn 30/100, 1–2 câu nguyên văn từ P1–P3. Hạn 11:30.
3. Sửa `reflection/doan-cong-hai.md`: bỏ phần khảo sát, sửa câu "gán nhãn tay dòng 1–50" cho khớp sự thật (AI gán, Hải kiểm). Nộp PR. Hạn 23:59.

## Lê Ngọc Khánh (đội trưởng) · cải tiến, báo cáo, người dùng thử, nộp bài

1. Sửa prompt phân loại cho `sai_mon` (ghi món đã đặt, không ghi món nhận nhầm) — cải tiến cho lượt 2.
2. Sửa `cost/personas.yaml`: thêm giá `gpt-4o-mini` (model đang chạy) và một model mạnh hơn; bỏ `gemini-2.5-flash` (bảng giá của đề ghi đã ngừng).
3. **Người dùng thử (bonus +5)** → `validation/log.md`: mời 3–5 bạn **ngoài nhóm** gõ thử khiếu nại vào bản chạy thử (`python run.py` trên máy Khánh với key tự chuẩn bị; gõ tin nhắn sau dấu `>`, Enter 2 lần để thoát). Đưa họ bảng đơn có sẵn để tự viết khiếu nại:

   | Mã đơn | Món trong đơn |
   |---|---|
   | A101 | Trà sữa trân châu 35k · Trà đào cam sả 40k · Bánh flan 15k |
   | A102 | Bún bò đặc biệt ×4 · Bún bò Huế ×4 · Chả cua thêm |
   | A104 | Combo gà rán 2 miếng · Pepsi (giao trễ 45 phút) |
   | A106 | Trà sữa trân châu · Bánh flan ×2 |
   | A108 | Combo gà rán 2 miếng ×3 · Khoai tây chiên ×2 |

   Ghi cho từng người: gõ gì · hệ thống trả gì · có hiểu, có tin không · muốn đổi gì · ≥1 câu nguyên văn. Không ghi tên. Hạn 12:30.
4. `eval/report.md` (lượt 1 → lượt 2, ≥3 lỗi, đã sửa gì, lỗi còn lại) · cập nhật `eval/README.md`.
5. `cost/cost-estimate.md` (3 kịch bản, chi phí / task thành công) · `spec.md` §8, §9.
6. Merge PR, nhắc tiến độ 10:30 và 12:30 · nộp CP4 trước 14:30.

## Sau CP4 (hạn 23:59)

- Mọi thay đổi sau 14:30 ghi vào `spec.md` §10.
- Mỗi người 1 file `reflection/<ten>.md` (mẫu `reflection/TEMPLATE.md`).

---

# (Đã xong) Phân công CP3 (hạn 10:00 Thứ Bảy 28/11)

> CP2 đã nộp 19:30 Thứ Sáu 27/11. **Từ giờ KHÔNG sửa `spec.md` §7 và `eval/metric_spec.yaml`** (sửa → khối đánh giá 0 điểm).
> Không sửa đáp án (`expected`) của câu thử đã có. Thêm câu mới thì được, ghi vào changelog `spec.md` §10.
> Không sửa `data/mock/` hay luật trong `policy.json` (đáp án câu thử dựa vào đó). Sửa `data/` hoặc `codebase/` xong → chạy `python eval/check_decisions.py`, phải ra 0 câu trượt.
> Mỗi việc: tạo nhánh mới từ `main` → commit → push → pull request. Khánh merge.

**CP3 cần:** bằng chứng đạt ngưỡng ≥1 nguồn · 20–30 câu thử (đã có 27) · **video 30 giây gọi AI thật** · kết quả lượt 1.
**Không có video gọi AI thật → không được xét giải.**

## Hồ An Lộc · nối model thật, lượt 1, video (VIỆC GẤP NHẤT)

1. Lấy API key (Gemini / OpenRouter / Groq, gói miễn phí). `copy .env.example .env`, điền `MODEL_PROVIDER`, `MODEL_NAME`, `API_KEY`. **Không commit `.env`, không để lộ key trong video.**
2. `python run.py eval --try` → thấy 3 câu chạy với model thật.
3. **Lượt 1:** `python run.py eval` → `eval/run-1.csv` + `traces/run-1.jsonl`, rồi `python eval/grade.py eval/run-1.csv` và `python run.py score eval/run-1.csv`.
   Commit cả `eval/run-1.csv` và `traces/run-1.jsonl` (bắt buộc nộp). Không chạy lại lượt 1 để lấy kết quả đẹp hơn.
4. **Video 30 giây:** chạy `python run.py`, gõ 2–3 tin nhắn (vd `đơn #A101 thiếu 1 ly trà sữa`, `don #A115 thieu 1 ly tra dao cam sa`, một câu tấn công), thấy câu trả lời thật + dòng `(model: … · token …)`. Để link video (Drive / YouTube không công khai) vào `eval/README.md`.
5. Hạn: tối nay. Kẹt key thì báo nhóm ngay.

## Đoàn Công Hải · bằng chứng từ người dùng

1. **Gửi form khảo sát** (bản đề xuất 11 câu, 4 phần, có chuyển phần) lên Discord lớp / nhờ các nhóm khác điền. Mục tiêu **≥20 người ngoài nhóm**, chốt 9:00 sáng mai.
   Xuất CSV từ Google Forms → gửi Khánh (hoặc lưu `evidence/survey/raw-responses.csv`; file `raw-*` không được commit).
2. **Gán nhãn tay dòng 1–50** trong `evidence/label_sample.csv`: tự đọc, **không dùng AI**, không mở `evidence/labels/khanh.csv` trước khi xong. Cột `label`: `co` / `khong` / `khong_ro` theo định nghĩa trong `evidence/data-mining.md` §1. Cột `nguoi_gan`: `Hai`.
3. **Phỏng vấn 3 người ngoài nhóm** về lần đơn đồ ăn gặp trục trặc **trong 1 tháng qua**: đã làm gì, nhắn ai, mất bao lâu, kết quả. Mỗi người một file `evidence/interviews/P1.md`… theo `TEMPLATE.md`, không ghi tên, có ít nhất 1 câu nguyên văn.
   Mẹo: mời người đã điền khảo sát và chọn "trong 1 tuần" / "1–4 tuần".
4. Hạn: nhãn tối nay; khảo sát và phỏng vấn trước 9:00 sáng mai.

## Nguyễn Quốc Quang Anh · chi phí, hỗ trợ phỏng vấn

1. `python run.py simulate --try` (10 phiên) để kiểm `cost/personas.yaml` chạy được. Bản đầy đủ (`python run.py simulate`) để sau khi có model thật và lượt 1 (CP4).
2. Hỗ trợ Hải phỏng vấn 1–2 người (cùng mẫu `evidence/interviews/TEMPLATE.md`).
3. Ghi góp ý về data giả / luật vào mục "Giới hạn" trong `data/DATA_CARD.md` (không sửa file JSON).

## Lê Ngọc Khánh (đội trưởng) · tổng hợp và nộp

1. Merge PR của mọi người; nhắc tiến độ lúc 22:00 tối nay và 8:30 sáng mai.
2. Khi có nhãn của Hải + CSV khảo sát: đếm theo cách đã ghi trước, viết `evidence/summary.md`.
3. Cập nhật số mới vào `canvas.md` dòng 4 và `spec.md` §1, §2 (thay số *tự ước tính* bằng số khảo sát nếu có).
4. Điền kết quả lượt 1 vào `spec.md` §7 dòng "Kết quả" (chỉ dòng này) và `eval/README.md`.
5. Nộp form CP3 trước 10:00.

---

# (Đã xong) Phân công CP2 (hạn 19:30 Thứ Sáu 27/11)

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
