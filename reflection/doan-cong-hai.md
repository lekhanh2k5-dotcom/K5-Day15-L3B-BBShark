# Reflection — Đoàn Công Hải

1. **Vai trò + phần mình làm:**
   Thành viên nhóm, phụ trách bằng chứng từ người dùng: phỏng vấn, gán nhãn review (`TEAMS.md`, `canvas.md` dòng 7), và ở CP4 là số liệu quy mô cho phần chi phí (`cost/scale-sources.md`).
   Dòng 1–50 trong `evidence/label_sample.csv` do AI gán nhãn trước, mình kiểm lại từng dòng (commit `f069c85`, nhánh `hai/nhan-1-50`). Kết quả: 13 `co`, 35 `khong`, 2 `khong_ro`, lý do từng dòng ghi ở cột `ghi_chu`. Mình cũng phỏng vấn người ngoài nhóm (`evidence/interviews/P1.md`–`P3.md`: 3 người, ngày 27/11).
   Phần khó nhất với mình là phân biệt rạch ròi giữa review chỉ phàn nàn chung (giao chậm, không bấm được nút huỷ trên app) với review thực sự có khiếu nại CSKH không thoả đáng, vì câu chữ của khách thường ngắn, viết tắt hoặc thiếu ngữ cảnh. Khi kiểm nhãn AI gán, đây cũng là chỗ mình phải đọc lại kỹ nhất.

2. **AI hỗ trợ mình thế nào:**
   - Nhãn dòng 1–50: AI gán nhãn trước kèm lý do ở cột `ghi_chu`, sau đó mình kiểm lại từng dòng theo định nghĩa ở `evidence/data-mining.md` §1 (`nguoi_gan` = "AI gán, Hải kiểm"). Trên 10 dòng chung (1–10), bản của mình và bản của Khánh cho cùng nhãn 10/10. Cả hai bản đều do AI gán trước rồi người kiểm, nên đây **không phải** độ khớp giữa hai người gán độc lập (`evidence/summary.md`).
   - Số liệu quy mô (CP4): Claude Code tìm và mở các trang nguồn, mình kiểm lại số và link trước khi nộp. Không có số Việt Nam cho tỉ lệ đơn có sự cố, nên file ghi rõ số lấy từ khảo sát ở Mỹ hoặc *(tự ước tính)*.
   - Claude Code soạn sẵn kịch bản hỏi trong `P1.md`–`P3.md`. Phần ghi chép và câu nguyên văn là mình tự ghi khi phỏng vấn.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   Lượt 1 chỉ trượt câu **B02** (`thuong`): *"đơn A106 giao nhầm, mình đặt trà sữa trân châu mà nhận trà đào"*. Model nhận ra đúng là sai món, nhưng đưa "trà đào" (món nhận nhầm) vào danh sách món thay vì "trà sữa trân châu" (món đã đặt), nên code tính ra `tu_choi · 0đ` thay vì hoàn 35.000đ (`eval/README.md`, `traces/run-1.jsonl`).
   Mình học được hai điều. Thứ nhất, khách thật hay kể cùng lúc cả món đặt và món nhận, nên chỉ hiểu đúng loại sự cố thôi là chưa đủ mà phải tách rõ đối tượng bị thiếu/sai. Thứ hai, chuyện này giống lúc mình gán nhãn: một review có thể nhắc sự cố mà không nhắc khiếu nại, nên phải đọc kỹ từng phần chứ không đoán theo từ khoá; với các câu dễ nhầm vai trò như B02, prompt cần nêu rõ ví dụ phân biệt "món đã đặt" và "món nhận nhầm" thay vì để model tự suy.
