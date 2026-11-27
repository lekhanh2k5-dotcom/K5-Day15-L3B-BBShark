# Reflection — Đoàn Công Hải

1. **Vai trò + phần mình làm:**
   Thành viên nhóm, phụ trách bằng chứng từ người dùng: phỏng vấn, khảo sát, gán nhãn review (`TEAMS.md`, `canvas.md` dòng 7).
   Mình gán nhãn tay dòng 1–50 trong `evidence/label_sample.csv` (commit `f069c85`, nhánh `hai/nhan-1-50`), ra 13 `co`, 35 `khong`, 2 `khong_ro`, và ghi lý do từng dòng ở cột `ghi_chu`. Mình cũng tạo Google Form khảo sát (11 câu, 4 phần, có chuyển phần) và phỏng vấn người ngoài nhóm (`evidence/interviews/P1.md`–`P3.md`: 3 người, ngày 27/11).
   Phần khó nhất với mình là: phân biệt rạch ròi giữa review chỉ phàn nàn chung (giao chậm, không bấm được nút huỷ trên app) với review thực sự có khiếu nại CSKH không thoả đáng khi câu chữ của khách thường ngắn, viết tắt hoặc thiếu ngữ cảnh; ngoài ra việc thiết kế chuyển phần trên Google Form sao cho người chưa từng gặp sự cố không trả lời nhầm vào các câu hỏi sau cũng mất nhiều công chỉnh sửa.

2. **AI hỗ trợ mình thế nào:**
   - Nhãn dòng 1–50: AI gán nhãn trước kèm lý do ở cột `ghi_chu`, sau đó mình kiểm lại từng dòng theo định nghĩa ở `evidence/data-mining.md` §1 (`nguoi_gan` = "AI gán, Hải kiểm"), đạt độ khớp 10/10 trên 10 dòng chung với bản của Khánh.
   - Câu hỏi khảo sát: Claude Code rà form của nhóm, gợi ý thêm câu sàng lọc làm mẫu số, câu hỏi thời điểm, chuyển phần, và bỏ ô xin số điện thoại. Mình và Khánh chọn bản cuối (`docs/ai-usage.md`).
   - File khảo sát đầu tiên (20 dòng, điền 18:03–18:56 ngày 27/11): Claude Code kiểm thì thấy câu 11 là câu mẫu có đánh số ("Dịch vụ rất tốt #2"…), người chọn "Chưa từng gặp" / "Không báo" vẫn trả lời phần sau, và câu chọn nhiều tự mâu thuẫn. Nhóm **không dùng** 20 dòng này, phải làm lại form. Lý do có 20 dòng đó: đây là bản dữ liệu điền thử để kiểm tra cấu trúc xuất file của Google Form lúc ban đầu, chưa phải câu trả lời khảo sát thật của người dùng và chưa bật đúng logic chuyển phần.
   - Claude Code soạn sẵn kịch bản hỏi trong `P1.md`–`P3.md`. Phần ghi chép và câu nguyên văn là mình tự ghi khi phỏng vấn.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   Lượt 1 chỉ trượt câu **B02** (`thuong`): *"đơn A106 giao nhầm, mình đặt trà sữa trân châu mà nhận trà đào"*. Model nhận ra đúng là sai món, nhưng đưa "trà đào" (món nhận nhầm) vào danh sách món thay vì "trà sữa trân châu" (món đã đặt), nên code tính ra `tu_choi · 0đ` thay vì hoàn 35.000đ (`eval/README.md`, `traces/run-1.jsonl`).
   Mình học được hai điều. Thứ nhất, khách thật hay kể cùng lúc cả món đặt và món nhận, nên chỉ hiểu đúng loại sự cố thôi là chưa đủ mà phải tách rõ đối tượng bị thiếu/sai. Thứ hai, chuyện này giống lúc mình gán nhãn: một review có thể nhắc sự cố mà không nhắc khiếu nại, nên phải đọc kỹ từng phần chứ không đoán theo từ khoá; với các câu dễ nhầm vai trò như B02, prompt cần nêu rõ ví dụ phân biệt "món đã đặt" và "món nhận nhầm" thay vì để model tự suy.
