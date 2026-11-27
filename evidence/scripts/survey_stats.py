"""Đếm kết quả khảo sát theo ngưỡng ghi trước ở evidence/hypothesis.md.

Chạy: python evidence/scripts/survey_stats.py  (đọc evidence/survey/results.csv)
"""
import csv
import sys
from collections import Counter
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "survey" / "results.csv"
TRONG_3_THANG = {"Trong 1 tuần", "1–4 tuần", "1–3 tháng"}
TRONG_1_THANG = {"Trong 1 tuần", "1–4 tuần"}
CHO_TU_1_GIO = {"1 đến 24 giờ", "Trên 24 giờ", "Đến giờ chưa có"}
KET_QUA_XAU = {"Chỉ xin lỗi", "Bị từ chối", "Chưa có kết quả"}
LUA_CHON_Q7 = ["Trợ lý hiểu đúng ngay", "Phải bấm qua nhiều nút hoặc điền form",
               "Trợ lý không hiểu, phải gõ lại", "Phải chờ chuyển sang nhân viên",
               "Tôi không dùng trợ lý tự động"]


def ket_qua(r):
    return {x.strip() for x in r["q9"].split(",") if x.strip()}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = list(csv.DictReader(open(PATH, encoding="utf-8-sig")))
    n = len(rows)
    gap3 = [r for r in rows if r["q2"] in TRONG_3_THANG]
    gap1 = [r for r in rows if r["q2"] in TRONG_1_THANG]
    bao = [r for r in rows if r["q5"] == "Có"]
    xau = [r for r in bao if r["q8"] in CHO_TU_1_GIO or (ket_qua(r) and ket_qua(r) <= KET_QUA_XAU)]
    bot = [r for r in bao if "Trợ lý tự động" in r["q6"]]

    print(f"n = {n}")
    print(f"Ngưỡng 1 · gặp trục trặc trong 3 tháng qua: {len(gap3)}/{n} (cần ≥ 1/3)")
    print(f"  trong 1 tháng qua: {len(gap1)}/{n}")
    print(f"Đã báo sự cố: {len(bao)}/{len(gap3) + sum(r['q2'] == 'Hơn 3 tháng' for r in rows)} người từng gặp")
    print(f"Ngưỡng 2 · chờ ≥1 giờ hoặc chỉ xin lỗi / bị từ chối / chưa có kết quả: {len(xau)}/{len(bao)} (cần ≥ 1/2)")
    print(f"Q8 thời gian (người đã báo): {dict(Counter(r['q8'] for r in bao))}")
    print(f"Q10 hài lòng 1–5 (người đã báo): {dict(sorted(Counter(r['q10'] for r in bao).items()))}")
    print(f"Có dùng trợ lý tự động: {len(bot)}/{len(bao)}")
    for opt in LUA_CHON_Q7:
        print(f"  Q7 '{opt}': {sum(opt in r['q7'] for r in bot)}/{len(bot)}")
    print(f"Q4 trục trặc: {dict(Counter(r['q4'] for r in rows if r['q4']))}")


if __name__ == "__main__":
    main()
