# Người dùng thử *(bonus)*

> 28/11/2026, khoảng 13:50–14:10. 2 người ngoài nhóm, mỗi người khoảng 10 phút, theo 5 nhịp (guide 4.3): làm quen · bối cảnh · giao việc · quan sát · hỏi sau.
> Bản chạy thử: `python run.py` trên máy Khánh, model `openai/gpt-4o-mini` qua OpenRouter, code ở `main` sau lượt 2. Người thử xem thẻ gồm bảng đơn A101–A108 và 2 việc giao theo kết quả, không có câu mẫu.
> Không ghi tên, chỉ ghi vai. Hệ thống trả gì chép từ màn hình.

| Người thử (vai) | Việc giao (theo kết quả, không theo nút) | Quan sát (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai) | Trích nguyên văn | Mức nghiêm trọng (cao / vừa / thấp) |
|---|---|---|---|---|
| **N1** · nội trợ khoảng 45 tuổi, ít dùng app, gõ có dấu, xưng "chị" | (1) Đơn A101 bị thiếu ly trà sữa, muốn được hoàn tiền | Gõ *"Chào em, chị đặt đơn A101 mà không thấy ly trà sữa đâu cả"* (không dùng chữ "thiếu") → bot hỏi *"Món nào chị không thấy?"* (`hoi_lai`), dù A101 chỉ có 1 món trà sữa. Trả lời *"Ly trà sữa trân châu đó em"* → bot **quên mã đơn** và hỏi lại *"Bạn gửi giúp mình mã đơn…"*, đổi xưng hô từ "chị" sang "bạn". Hỏi người điều phối *"chị nói mã đơn rồi mà, nó hỏi lại làm gì?"* rồi **bỏ ngang** việc 1. | "chị nói rồi mà nó cứ hỏi lại" | **cao**: bỏ ngang, không được hoàn |
| N1 | (2) Đơn A108 gần như không nhận được gì, muốn hoàn lại tiền | Gõ *"Đơn A108 của chị gần như không nhận được gì, em hoàn lại tiền cho chị nhé"* → bot hỏi *"Bạn có thể cho biết món nào bị thiếu không?"*. "Gần như không nhận được gì" không được hiểu là cả đơn, nên chưa tới bước chuyển nhân viên. | "thôi chị gọi tổng đài cho nhanh" | **cao**: khách chuyển sang kênh khác |
| **N2** · nhân viên IT khoảng 25 tuổi, đặt gần như mỗi ngày, gõ nhanh, viết tắt, sai chính tả | (1) Đơn A101 thiếu trà sữa, muốn hoàn tiền | Gõ *"#A101 thiu tra sua tran chau r, refund dc k"* → bot hỏi *"Bạn thiếu món gì?"*: hỏi lại đúng thứ khách đã ghi (chỉ sai chữ "thiu"). | "ghi trà sữa trân châu rồi còn gì, bot đọc không vậy?" | **vừa** |
| N2 | (2) Đơn A108 thiếu gần hết, muốn hoàn toàn bộ | Gõ *"A108 thieu 3 combo ga + 2 khoai, refund full nha"* → **chuyển nhân viên đúng** (vượt hạn mức). Nhưng lời nhắn không nói lý do, cũng không nói phải chờ bao lâu. | "ok rồi chờ bao lâu? 5 phút hay 1 tiếng?" | **thấp** |
| N2 | (thêm, khó hơn) A101 thiếu 2 món cùng lúc; mã đơn sai | *"A101 thiếu bánh flan với trà đào"* → hỏi lại *"món nào bị thiếu"*, không xử lý được 2 món có tên viết ngắn. *"A999 thiếu trà sữa"* → *"Mình không tìm thấy đơn A999. Bạn kiểm tra lại mã đơn trong mục Đơn hàng giúp mình nhé."*, người thử nói *"cái này ổn"*. | "đơn lớn thì nó chuyển người được, đơn nhỏ lại hỏi tới hỏi lui" | **vừa** (2 món) · không lỗi (mã sai) |

Câu hỏi sau: *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* → rất tiếc 0 / hơi tiếc 1 (N2) / không sao 1 (N1)

## Tổng hợp

- **Chủ đề lặp nhiều nhất: bot hỏi lại thứ khách đã nói** (gặp ở cả 2 người, 4/6 lượt gõ). Có 3 nguyên nhân:
  1. **Tên món viết ngắn không khớp** với tên trong đơn ("trà sữa" → "Trà sữa trân châu", "trà đào" → "Trà đào cam sả"), **kể cả khi gõ có dấu** và đơn chỉ có 1 món cùng loại. Đây là lỗi B07/B27 trong `eval/report.md`, xuất hiện sau khi sửa prompt ở lượt 2. Người thật gặp nó ngay ở việc đầu tiên.
  2. **Bot không nhớ câu trước.** Mỗi tin nhắn được xử lý riêng, nên khách trả lời câu hỏi lại của bot thì bị quên mã đơn. Câu hỏi lại theo mẫu cứng còn đổi xưng hô "chị" thành "bạn".
  3. **Cách nói cả đơn** ("gần như không nhận được gì") và **nhiều món trong 1 câu** không được hiểu.
- **Đúng giả thuyết pain:** khi bot hỏi vòng vo, người thử bỏ sang tổng đài, đúng như review "chatbot vòng vo" (`evidence/summary.md`). Phần tính tiền và hạn mức không sai lần nào. Lỗi nằm ở khâu **hiểu tin nhắn và giữ hội thoại**.
- **Sửa gì trước demo:** **không sửa code trước 14:30.** Lượt 2 đã chạy và chốt trên code hiện tại, sửa ngay lúc này mà không chạy lại thì kết quả lượt 2 không còn khớp với code. Thay vào đó, khi demo nhóm gõ câu có đủ mã đơn và tên món, và nói rõ lỗi này trên slide 5 và 8. Ghi `spec.md` §10.
- **Thay đổi rút ra (làm sau CP4, ghi changelog khi làm):**
  1. Khớp tên món ở code: so khớp mờ, bỏ dấu, nhận tên ngắn nếu đơn chỉ có 1 món chứa tên đó. Bỏ yêu cầu "phải có trong DANH SÁCH MÓN" khỏi prompt `thieu_mon`.
  2. Giữ mã đơn của lượt trước trong cùng phiên, để khách trả lời câu hỏi lại không phải khai lại.
  3. Lời nhắn chuyển nhân viên nêu lý do (vượt hạn mức 200.000đ) và thời gian chờ dự kiến.
  4. Thêm câu thử từ chính các câu người thử đã gõ vào bộ câu thử sau (nguồn `nguoi_dung`).
- **Giữ gì và vì sao:**
  - Báo mã đơn sai kèm chỗ xem mã (A999): rõ ràng, người thử khen.
  - Chuyển nhân viên khi vượt hạn mức (A108): đúng chính sách dù khách viết tắt.
  - Code quyết định số tiền: không có lần nào hoàn sai hay vượt hạn mức.
- **Để dành sau:** tự lấy mã đơn từ màn hình đơn hàng trong app, thay vì bắt khách nhớ và gõ mã.
