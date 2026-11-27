# Thống kê review đã cào

> Sinh bởi `evidence/scripts/review_stats.py` từ `evidence/raw-reviews.csv` (review công khai Google Play, tải 27/11/2026). Chủ đề đếm bằng từ khoá, còn thô.

## 1. Theo app

| App | N | Từ | Đến | 1★ | 2★ | 3★ | 4★ | 5★ | Sao TB |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| ShopeeFood | 10000 | 2025-01-06 | 2026-11-26 | 3536 | 213 | 222 | 343 | 5686 | 3.44 |
| Grab | 3000 | 2026-08-13 | 2026-11-26 | 1806 | 75 | 71 | 51 | 997 | 2.45 |
| be | 3000 | 2025-11-21 | 2026-11-26 | 1599 | 101 | 99 | 73 | 1128 | 2.68 |
| XanhSM | 3000 | 2026-09-15 | 2026-11-26 | 944 | 99 | 104 | 172 | 1681 | 3.52 |

## 2. Phễu lọc

| Bước | Số review | % trên 19000 |
|---|---:|---:|
| Nhắc đồ ăn / đơn hàng | 3614 | 19.0% |
| Đồ ăn + sự cố hoặc xử lý khiếu nại | 1198 | 6.3% |
| … trong đó 1–2★ | 1127 | 94% của 1198 |
| Nói đúng thiếu / sai món | 64 | 0.3% |

## 3. Chủ đề trong 1198 review có sự cố

| Chủ đề | Số review | % |
|---|---:|---:|
| Huỷ đơn | 587 | 49% |
| Giao trễ, chờ lâu | 318 | 27% |
| Hỗ trợ / CSKH / tổng đài / chatbot kém | 326 | 27% |
| Đồ nguội, đổ, hỏng | 124 | 10% |
| Hoàn tiền chậm / không hoàn | 207 | 17% |
| Thiếu món, sai món | 52 | 4% |
| Bồi thường bằng voucher / mã giảm | 42 | 4% |

## 4. ShopeeFood theo tháng (review có sự cố / tổng review tháng đó)

| Tháng | Có sự cố | Tổng | % |
|---|---:|---:|---:|
| 2025-12 | 29 | 449 | 6% |
| 2026-01 | 23 | 334 | 7% |
| 2026-02 | 24 | 338 | 7% |
| 2026-03 | 47 | 384 | 12% |
| 2026-04 | 38 | 420 | 9% |
| 2026-05 | 73 | 524 | 14% |
| 2026-06 | 39 | 522 | 7% |
| 2026-07 | 25 | 467 | 5% |
| 2026-08 | 36 | 446 | 8% |
| 2026-09 | 39 | 471 | 8% |
| 2026-10 | 38 | 437 | 9% |
| 2026-11 | 14 | 274 | 5% |

Tháng cuối chỉ có dữ liệu đến ngày tải nên ít review hơn.
