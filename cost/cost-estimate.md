# Chi phí khi dùng thật

> Số đo lấy từ `python run.py simulate` (`cost/simulate-1-summary.md`, không điền tay). Quy mô thật lấy từ `cost/scale-sources.md` (Hải, có link nguồn).
> Giá tính theo **gói trả phí tiêu chuẩn**.

## 1. Đầu vào

- **Kiểu khách** (`cost/personas.yaml`, *tự ước tính*): 80% báo 1 lần/tháng (1 lượt hỏi), 15% báo 2 lần (2 lượt hỏi), 5% báo 3 lần (2 lượt hỏi).
- **Giá** (USD / 1 triệu token vào · ra, trang giá OpenAI xem 25/11/2026):

  | Model | Vào | Ra |
  |---|---:|---:|
  | gpt-4o-mini (model đang chạy) | 0,15 | 0,60 |
  | gpt-5-mini | 0,25 | 2,00 |
  | gpt-6.1-terra | 1,00 | 5,00 |

- **Mô phỏng:** `cost/simulate-1.csv`, run `simulate-1@20261128-103150`, 50 phiên, seed 42, model thật `gpt-4o-mini`, 0/50 phiên lỗi.
- **Tỉ lệ đạt:** 25/27 (93%) từ lượt 2 (`eval/run-2.csv`, `run-2@20261128-102345`).
- **Token đo trên `gpt-4o-mini`.** Giá của 2 model kia tính với cùng số token đó. Model khác dùng bộ tách token khác nên số thật có thể lệch.

## 2. Kết quả mô phỏng

Trung bình mỗi phiên: 509 token vào · 57 token ra · 1,4 lần gọi model (câu hỏi lại và câu chưa có mã đơn không gọi model).

| Model | Chi phí / phiên | **Chi phí / task thành công** |
|---|---:|---:|
| gpt-4o-mini | $0,00011 | **$0,00012** (≈ 3đ) |
| gpt-5-mini | $0,00024 | **$0,00026** (≈ 6,5đ) |
| gpt-6.1-terra | $0,00079 | **$0,00086** (≈ 21đ) |

Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt 93%, **không coi như đạt 100%**. Quy đổi 25.000đ/USD (cách quy đổi theo Tuổi Trẻ, xem `cost/scale-sources.md`).

## 3. Ba kịch bản ở quy mô thật

Số khiếu nại / tháng = số đơn / tháng × tỉ lệ đơn có sự cố × tỉ lệ có báo. Mỗi khiếu nại tính là một phiên.

| Kịch bản | Số khiếu nại / tháng | gpt-4o-mini | gpt-5-mini | gpt-6.1-terra |
|---|---:|---:|---:|---:|
| **Thấp**: chỉ 1 app (48% của 29,2 triệu đơn), sự cố 5%, báo 10% *(tự ước tính)* | ≈ 70.000 | **$8 / tháng** | $18 | $60 |
| **Cơ sở**: cả thị trường, sự cố 12% *(tự ước tính, ≈ ½ số Mỹ)*, báo 24% (eduMe) | ≈ 840.000 | **$100 / tháng** | $218 | $719 |
| **Cao**: cả thị trường, sự cố 24,4%, báo 31,4% (Zion & Zion, Mỹ) | ≈ 2,23 triệu | **$266 / tháng** | $579 | $1.907 |

Nguồn từng số: `cost/scale-sources.md` (Ken Research 350 triệu đơn năm 2025, Momentum Works thị phần 48%, Zion & Zion 2019, eduMe 2022).
Bảng 50 / 100 / 200 khách trong `cost/simulate-1-summary.md` là kịch bản thử nghiệm nhỏ ($0,008 – $0,03 / tháng với gpt-4o-mini), không phải quy mô thật.

**Giới hạn:** tỉ lệ sự cố và tỉ lệ báo là số ở Mỹ hoặc tự ước tính, chưa có số Việt Nam. Số đơn / tháng chênh khoảng 3 lần giữa hai cách tính (`cost/scale-sources.md`). Câu thử và phiên mô phỏng ngắn hơn hội thoại thật (thường 1–2 lượt), nên token thật có thể cao hơn.

## 4. So với impact

- **Impact theo `spec.md` §2:** khách bỏ ra khoảng 12,5 phút / tháng cho việc báo và theo dõi sự cố *(tự ước tính, phỏng vấn P1–P3: thao tác 10–15 phút, chờ 25 phút đến 3 giờ)*.
- **Chi phí model / người / tháng (cơ sở, gpt-4o-mini):** $0,00016 ≈ 4đ (`cost/simulate-1-summary.md`).
- **Chi phí ngoài model chưa tính:** nhân viên xử lý ca được chuyển (vượt hạn mức, ≥3 khiếu nại, sức khoẻ), hosting, lưu log. Ở mọi kịch bản, giờ công người cho các ca chuyển vẫn lớn hơn nhiều so với tiền model.
- **Kết luận: đáng làm.** Kể cả kịch bản cao với model đắt nhất, tiền model vẫn dưới $2.000 / tháng cho 2,23 triệu khiếu nại (≈ 21đ / khiếu nại). Rủi ro chính nằm ở chất lượng: lượt 2 đạt 93%, và lời nhắn còn lỗi (`eval/report.md`), chứ không nằm ở chi phí. Nên giữ gpt-4o-mini, đổi model khi độ chính xác trên bộ câu thử tăng rõ.

## 5. Độ nhạy (ngắn)

- Đổi gpt-4o-mini → gpt-6.1-terra: chi phí tăng khoảng 7 lần ($100 → $719 / tháng, kịch bản cơ sở).
- Số đơn theo cách tính thứ hai (≈ 91 triệu / tháng, gấp ~3 lần): kịch bản cơ sở thành ≈ $300 / tháng với gpt-4o-mini.
- Hội thoại thật dài gấp đôi token: chi phí gấp khoảng đôi, kết luận không đổi.
