# Tóm tắt mô phỏng simulate-1@20261128-103150

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| bao_mot_lan | 43 | 1 | 471 | 51 | 1.3 | 2.4 |
| bao_hai_lan | 4 | 2 | 742 | 90 | 2.2 | 2.8 |
| bao_ba_lan | 3 | 2 | 755 | 95 | 2.3 | 4.0 |

Tỉ lệ đạt dùng để tính: 25/27 (93%) — lượt run-2@20261128-102345

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (50 người) | Chi phí / tháng — cơ sở (100 người) | Chi phí / tháng — cao (200 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00011 | $0.00012 | $0.00010 | $0.0078 | $0.0156 | $0.0312 | $0.00016 |
| gpt-5-mini (vào 0.25 · ra 2.0 $/1M) | $0.00024 | $0.00026 | $0.00023 | $0.0171 | $0.0342 | $0.0683 | $0.00034 |
| gpt-6.1-terra (vào 1.0 · ra 5.0 $/1M) | $0.00079 | $0.00086 | $0.00075 | $0.0561 | $0.1121 | $0.2242 | $0.0011 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.1) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-4o-mini. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
