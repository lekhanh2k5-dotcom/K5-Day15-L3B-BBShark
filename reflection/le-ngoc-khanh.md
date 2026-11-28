# Reflection — Lê Ngọc Khánh

1. **Vai trò + phần mình làm:**
   Đội trưởng: chọn track D1, chia việc theo từng checkpoint (`TASKS.md`), duyệt và merge PR của cả nhóm, nộp 4 checkpoint.
   Phần mình trực tiếp làm hoặc duyệt từng dòng:
   - Data giả và bộ câu thử: `data/make_mock_data.py`, `eval/benchmark.csv` (27 câu), chuẩn "đạt" ở `spec.md` §7.
   - Nhãn dòng 51–100: AI gán trước, mình kiểm lại và sửa 3 dòng (`evidence/labels/khanh.csv`).
   - Cải tiến lượt 2: thêm quy tắc sai món trong prompt (PR #19).
   - Báo cáo và chi phí: `eval/report.md`, `cost/cost-estimate.md`, `spec.md` §8–§9 (PR #22, #24).
   - Người dùng thử 2 người ngoài nhóm: `validation/log.md` (PR #27).

2. **AI hỗ trợ mình thế nào:**
   Mình dùng Claude Code gần như suốt hackathon: soạn bản đầu của spec, code khung, script cào review, báo cáo; rà PR của thành viên; đọc trace để tìm lỗi.
   Chỗ phải sửa hoặc bỏ output của AI:
   - Regex an toàn bị ghi nhầm ký tự backspace thay cho `\b`.
   - Từ "ói" khớp nhầm vào "đói".
   - Script thống kê review lỗi vì dấu `%`.
   Có một chỗ mình **không** làm theo bản AI đưa: một bản ghi người dùng thử do AI đóng vai người thử. Mình không đưa vào `validation/log.md` vì đó không phải người thật.
   Tương tự, nhóm bỏ phần khảo sát vì không xác minh được phản hồi.
   Bài học: AI làm nhanh, nhưng mình phải là người quyết định cái gì được tính là bằng chứng.

3. **Một câu thử trượt của nhóm và mình học được gì:**
   Lượt 1 trượt **B02** (khách đặt trà sữa nhưng nhận trà đào): model ghi món nhận nhầm nên code từ chối khách. Mình sửa prompt, B02 đúng, câu `thuong` lên 6/6 và đạt chuẩn.
   Nhưng sửa xong thì **B07 và B27 tệ đi**: model hỏi lại dù khách đã nêu tên món. Lúc cho người thật dùng thử, lỗi này xuất hiện ngay ở việc đầu tiên, khi khách gõ "trà sữa" thay vì tên đầy đủ.
   Điều mình học được:
   - Sửa một lỗi bằng prompt có thể làm hỏng chỗ khác, nên phải chạy lại toàn bộ câu thử chứ không chỉ câu vừa sửa.
   - Bộ chấm chỉ đọc dòng quyết định nên bỏ sót lỗi ở lời nhắn; phải đọc trace và cho người thật dùng mới thấy.
   - Lần sau nên để code khớp tên món (bỏ dấu, nhận tên ngắn) thay vì bắt model làm việc đó.
