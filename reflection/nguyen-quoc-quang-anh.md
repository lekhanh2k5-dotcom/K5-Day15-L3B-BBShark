# Reflection — Nguyễn Quốc Quang Anh

## 1. Vai trò và phần mình làm

Mình thử luồng báo thiếu món trên ShopeeFood và chụp lại hai nhánh mà Tép Thám Tử đưa ra: chọn đơn hàng hoặc xem hướng hỗ trợ. [Ảnh hướng hỗ trợ](../docs/shopeefood-huong-ho-tro.jpg)
Từ quan sát đó, mình viết phần luồng hiện tại, so sánh các cách hỗ trợ và ghi rõ giả định khi tính thời gian khách bỏ ra để khiếu nại. [Spec §0, §2, §3](../spec.md)
Ở CP3 mình kiểm cấu hình chi phí bằng 10 phiên chạy thử với model giả. Đến CP4 mình đưa số đo 50 phiên do Lộc chạy và kết quả hai lượt đánh giá vào bộ slide 8 trang. [Commit slide CP4](https://github.com/lekhanh2k5-dotcom/K5-Day15-L3B-BBShark/commit/646fcfd)

## 2. AI hỗ trợ mình thế nào

Mình dùng Codex để tổng hợp tài liệu,\
dựng bảng so sánh\
và soạn slide từ các file của nhóm

## 3. Một câu thử trượt và điều mình học được

Ở B02, khách đặt trà sữa trân châu nhưng nhận trà đào. Lượt 1 nhận ra lỗi giao sai món, rồi lại tra giá trà đào nên từ chối hoàn tiền. [Kết quả lượt 1](../eval/run-1.csv)
Sau khi nhóm sửa hướng dẫn để model lấy tên món khách đã đặt, B02 trả đúng 35.000đ. Cùng lượt đó, B07 và B27 lại trượt, khiến tổng số câu đúng giảm từ 26 xuống 25 trên 27. [Kết quả lượt 2](../eval/run-2.csv)
Khi trình bày kết quả, mình cần giải thích cả hai con số: ca sai món đã được sửa, nhưng hai khách khác lại bị hỏi thêm. Chỉ nhìn điểm tổng thì dễ bỏ sót cả điều đã tốt lên lẫn điều khách vẫn còn vướng.
