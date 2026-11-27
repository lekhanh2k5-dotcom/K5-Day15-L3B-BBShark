"""Kiểm phần CODE ra quyết định (không gọi model): thay bước phân loại của model bằng đáp án đúng,
rồi xem code có ra đúng [quyet_dinh] cho cả bộ câu thử không.

    python eval/check_decisions.py

Chạy lệnh này mỗi khi sửa data/mock/, data/make_mock_data.py, codebase/tools.py hoặc codebase/agent.py.
Kết quả phải là "0 câu trượt". Có câu trượt = data hoặc code vừa sửa đã làm sai đáp án của câu thử đó.
Đây KHÔNG phải một lượt đánh giá (không gọi model, không ghi run-N.csv) — chỉ là kiểm thử code.
Phân loại đúng cho từng câu (TRUTH) do nhóm viết tay từ cột input, không lấy từ output của model.
"""
import csv
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "codebase"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import tracing  # noqa: E402
import agent  # noqa: E402
from grade import grade_row  # noqa: E402

# id câu thử → (loại sự cố, các món khách nêu) — đúng như một bộ phân loại hoàn hảo sẽ trả
TRUTH = {
    "B01": ("thieu_mon", ["Trà sữa trân châu"]), "B02": ("sai_mon", ["Trà sữa trân châu"]),
    "B03": ("giao_tre", []), "B05": ("giao_tre", []), "B06": ("thieu_mon", ["Bún bò Huế"]),
    "B07": ("thieu_mon", ["bánh tráng trộn"]), "B08": ("thieu_mon", ["Trà sữa trân châu"]),
    "B09": ("thieu_mon", ["Canh chua"]),
    "B10": ("thieu_mon", ["Combo gà rán 2 miếng", "Combo gà rán 2 miếng", "Khoai tây chiên"]),
    "B11": ("thieu_mon", ["Trà đào cam sả"]), "B12": ("chua_ro", []), "B13": ("khac", []),
    "B14": ("thieu_mon", []), "B18": ("giao_tre", []), "B19": ("thieu_mon", ["Pepsi"]),
    "B20": ("thieu_mon", ["Trà đào cam sả"]), "B21": ("thieu_mon", ["Khoai tây chiên"] * 3),
    "B22": ("chua_ro", []), "B23": ("thieu_mon", ["Cơm tấm sườn"]), "B24": ("thieu_mon", ["Bún bò Huế"]),
    "B04": ("chua_ro", []), "B15": ("chua_ro", []), "B16": ("chua_ro", []), "B17": ("chua_ro", []),
    "B25": ("giao_tre", []), "B26": ("thieu_mon", ["Trà đào cam sả"]), "B27": ("thieu_mon", ["Khoai tây chiên"]),
}


def main():
    cur = {}
    agent._classify = lambda text, order: {"issue": cur["v"][0], "items": cur["v"][1], "ask": ""}
    rows = list(csv.DictReader(open(os.path.join(ROOT, "eval", "benchmark.csv"), encoding="utf-8-sig")))
    missing = [r["id"] for r in rows if r["id"] not in TRUTH]
    bad = 0
    for r in rows:
        cur["v"] = TRUTH.get(r["id"], ("chua_ro", []))
        tracing.begin("check")
        out = agent.answer(r["input"])["output"]
        tracing.end()
        g = grade_row({"expected": r["expected"], "output": out})
        if not g["ok"]:
            bad += 1
            print("TRƯỢT %s: %s | %s" % (r["id"], g["notes"], out.splitlines()[-1]))
    print("%d câu thử · %d câu trượt" % (len(rows), bad))
    if missing:
        print("(Câu chưa có phân loại đúng trong TRUTH, đang coi là chua_ro: %s — thêm vào TRUTH khi viết câu thử mới.)"
              % ", ".join(missing))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
