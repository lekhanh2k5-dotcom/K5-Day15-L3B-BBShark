# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

Ba kiểu khách lần lượt chiếm 80%, 15% và 5%, dùng 1, 2 và 3 phiên/tháng. Số lượt hỏi mỗi phiên lần lượt là 1, 2 và 2. Ba kịch bản triển khai có 50, 100 và 200 khách dùng mỗi tháng *(tự ước tính)*. [Cấu hình](personas.yaml) · [Căn cứ kịch bản tại §2](../spec.md)

Giá trả phí tiêu chuẩn, USD/triệu token văn bản vào và ra: Gemini 2.5 Flash-Lite 0,10 và 0,40; Gemini 2.5 Flash 0,30 và 2,50. Ngày tra 27/11/2026. [Bảng giá Google](https://ai.google.dev/gemini-api/docs/pricing)

Mô phỏng dùng 50 phiên, seed 42. Model đo token và tỉ lệ đạt sẽ lấy từ lượt chạy thật và lượt 2 đã chấm.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · __ phiên · seed __

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng theo §2: 12,5 phút khách bỏ ra (tự ước tính). Thời gian tiết kiệm thực tế chưa đo.
- Chi phí / người / tháng (cơ sở, model __): __
- **Kết luận một dòng — đáng làm không:** __

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
