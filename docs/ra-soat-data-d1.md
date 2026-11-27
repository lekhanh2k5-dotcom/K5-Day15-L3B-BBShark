# Góp ý dữ liệu giả cho lát cắt D1

Đối chiếu [data card](../data/DATA_CARD.md) với ba file trong [data/mock](../data/mock/) ngày 27/11/2026.

| Quan sát trong dữ liệu | Ý nghĩa khi đọc kết quả |
|---|---|
| 30 đơn thuộc 21 mã khách khác nhau. 29 đơn đã giao, riêng A107 đang giao và chưa có thời điểm giao thực tế. | Có thể thử nhánh báo thiếu món khi đơn còn trên đường. Khoảng mã K01–K30 không tương ứng với 30 người dùng riêng biệt trong tập đơn. |
| Chính sách cấp voucher khi trễ **quá** 30 phút. A103 trễ 29 phút và A104 trễ 45 phút. Trong 30 đơn chưa có ca trễ đúng 30 phút. | Khi rà chính sách, cần phân biệt đúng 30 phút (xin lỗi) với 31 phút (đề xuất voucher). Đây là chỗ dữ liệu hiện chưa thử sát ranh giới. |
| Trong 9 khiếu nại cũ, K05 có 5 lần. Chính sách chuyển người từ 3 lần trong 30 ngày. | K05 thử được phía vượt ngưỡng. Có thể kiểm thêm 2 lần và đúng 3 lần ở bộ dữ liệu phát triển để biết hệ thống chuyển đúng thời điểm. |
| Mỗi món ghi tên, số lượng và đơn giá. Đơn có phí giao riêng. Không có giá topping, giảm giá theo món hoặc phân bổ voucher. | Đề xuất hoàn phần thiếu trong demo có căn cứ từ giá món đã ghi. Với đơn thực tế có khuyến mãi, còn cần biết số tiền thực trả cho từng món trước khi áp dụng phép tính này. |

Các ngưỡng tiền, thời gian và lịch sử khiếu nại là quy tắc dựng của nhóm. Các phép đếm trên mô tả độ phủ của dữ liệu thử.
