# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử: `agent.py`, `tools.py` | Claude Code · Antigravity | Viết workflow, 7 công cụ, chặn an toàn, kiểm số tiền trong lời nhắn; hỗ trợ dọn trùng merge và bổ sung lọc không dấu | Khánh chạy `run.py`, `eval/check_decisions.py` (27/27); Lộc rà soát, dọn bản trùng sau merge (PR #11), bổ sung bắt `SAFETY`/`WANT_HUMAN` không dấu (không bắt nhầm món "sườn non") và chạy smoke test kiểm chứng | Khánh · Lộc |
| Nối model `ai.py` | Claude Code (bản đầu) · Antigravity | Viết và gộp lời gọi Gemini / OpenRouter / Groq / OpenAI / Claude / Ollama bằng thư viện chuẩn (`temperature=0`) | Lộc gộp bản cuối (PR #11), tự tạo `.env`, chạy `eval --try`, chạy thật Lượt 1 (`run-1`), Lượt 2 (`run-2`), `simulate` trên `gpt-4o-mini` và quay video kiểm chứng | Lộc |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Soạn prompt phân loại (JSON) và prompt viết lời nhắn | Khánh duyệt; sẽ đánh giá qua lượt 1 | Khánh |
| Đào data: script cào, lọc, thống kê review | Claude Code | Viết `scrape_reviews.py`, `review_stats.py`, cách đếm, bảng số | Khánh kiểm số đếm và sửa bộ từ khoá bị đếm thừa ("đổ" khớp "đổi") | Khánh |
| Gán nhãn review | AI *(Khánh ghi tên công cụ)* · Antigravity | AI gán nhãn trước dòng 1–10, 51–100 (Khánh) và dòng 1–50 (Hải) kèm lý do | **Khánh kiểm 60/60 dòng** (`evidence/labels/khanh.csv`); soát lại theo định nghĩa đã ghi trước, sửa 3 dòng (51, 64, 88); số dòng sửa ở lần kiểm đầu: __ · **Hải kiểm 50/50 dòng** 1–50 (`evidence/label_sample.csv`); độ khớp 10 dòng đầu: 10/10 | Khánh · Hải |
| Phỏng vấn: trình bày ghi chép | Claude Code | Soạn sẵn 5 câu hỏi trong `P1.md`–`P3.md`; chia ghi chép Hải gửi thành gạch đầu dòng, sửa câu chữ cho gọn (giữ nguyên từng chữ câu trích nguyên văn) | Hải hỏi và ghi cả 3 cuộc; nội dung là lời người được phỏng vấn kể | Hải |
| Viết câu thử (benchmark) | Claude Code | Soạn 27 câu từ tình huống khó trong đề Track D; 9 câu dùng nguyên văn / viết lại từ review thật (cột `source` ghi rõ) | Khánh duyệt; câu thử không sửa đáp án sau khi chạy | Khánh |
| Sinh data `synthetic` | Claude Code | Viết `data/make_mock_data.py` | Seed 15 · kiểm tay 8 đơn viết tay A101–A108 và đáp án các câu thử dùng chúng (`eval/check_decisions.py`) | Khánh |
| Chấm cột `pass` | Không dùng LLM | — | Chấm bằng code: `eval/grade.py` | — |
| `spec.md` §1, §4, §7, `evidence/data-mining.md`, `data/DATA_CARD.md`, `eval/metric_spec.yaml` | Claude Code | Soạn bản đầu | Khánh duyệt; cả nhóm duyệt chuẩn "đạt" 19:00 27/11 | Khánh |
| `spec.md` §0, §2, §3, `cost/` | Codex | Đối chiếu ảnh với luồng ShopeeFood, tìm nguồn cho bảng impact và so sánh dịch vụ, chuẩn bị cấu hình persona và chạy thử 10 phiên | Quang Anh cung cấp ảnh từ tài khoản của mình. Bản nộp dùng hai ảnh không hiện tên tài khoản. | Quang Anh |
| `spec.md` §5, §6, sơ đồ `docs/ai-architecture.svg` | Antigravity | Soạn bảng 9 kịch bản khó/tấn công ở §5, 4 đường đi trải nghiệm ở §6 theo `benchmark.csv` và tạo sơ đồ vector `docs/ai-architecture.svg` | Lộc đối chiếu khớp 1-1 với luồng `agent.py`, 7 công cụ `tools.py` và 27 câu thử, kiểm XML hợp lệ và merge ở PR #11 | Lộc |
| Slide, văn bản | Codex | Dựng bản PDF 8 trang từ bằng chứng, hai lượt đánh giá và kết quả mô phỏng 50 phiên của nhóm | Duyệt nội dung, lời demo và số liệu trước khi nộp | Quang Anh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
