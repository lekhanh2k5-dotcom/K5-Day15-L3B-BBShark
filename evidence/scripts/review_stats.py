"""Thống kê review đã cào → evidence/review_stats.md (chạy sau scrape_reviews.py).

    python evidence/scripts/review_stats.py

Đọc evidence/raw-reviews.csv (không commit). Chủ đề đếm bằng từ khoá nên còn thô; một review có thể thuộc nhiều chủ đề.
"""
import collections
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EVID = os.path.dirname(HERE)
APPS = ["ShopeeFood", "Grab", "be", "XanhSM"]
TOPICS = {
    "Huỷ đơn": r"hủy đơn|huỷ đơn|bị hủy|bị huỷ|tự hủy|tự huỷ",
    "Giao trễ, chờ lâu": r"trễ|giao chậm|giao lâu|chờ lâu|đợi lâu|cả tiếng|tiếng rưỡi|\d+\s*tiếng",
    "Hỗ trợ / CSKH / tổng đài / chatbot kém": r"hỗ trợ|ho tro|cskh|chăm sóc|tổng đài|chatbot|chat bot|phản hồi|không trả lời|ko trả lời|kh trl",
    "Đồ nguội, đổ, hỏng": r"nguội|\bđổ\b|đổ hết|bị đổ|hỏng|\bôi\b|thiu",
    "Hoàn tiền chậm / không hoàn": r"hoàn tiền|hoan tien|hoàn lại|chưa hoàn|ko hoàn|không hoàn|treo tiền",
    "Thiếu món, sai món": r"thiếu món|thiếu đồ|giao thiếu|làm thiếu|sai món|nhầm món|giao nhầm|giao sai",
    "Bồi thường bằng voucher / mã giảm": r"voucher|vorcher|mã giảm",
}


def main():
    rows = list(csv.DictReader(open(os.path.join(EVID, "raw-reviews.csv"), encoding="utf-8-sig")))
    out = ["# Thống kê review đã cào", "", "> Sinh bởi `evidence/scripts/review_stats.py` từ `evidence/raw-reviews.csv` "
           "(review công khai Google Play, tải 27/11/2026). Chủ đề đếm bằng từ khoá, còn thô.", ""]
    out += ["## 1. Theo app", "", "| App | N | Từ | Đến | 1★ | 2★ | 3★ | 4★ | 5★ | Sao TB |", "|---|---:|---|---|---:|---:|---:|---:|---:|---:|"]
    for a in APPS:
        x = [r for r in rows if r["app"] == a]
        st = collections.Counter(int(r["score"]) for r in x)
        d = sorted(r["date"] for r in x)
        out.append("| %s | %d | %s | %s | %s | %.2f |" % (a, len(x), d[0], d[-1], " | ".join(str(st[s]) for s in range(1, 6)),
                                                         sum(int(r["score"]) for r in x) / len(x)))
    fi = [r for r in rows if r["food_issue"] == "1"]
    food = sum(r["food"] == "1" for r in rows)
    strict = sum(r.get("thieu_sai_mon") == "1" for r in rows)
    out += ["", "## 2. Phễu lọc", "", "| Bước | Số review | %% trên %d |" % len(rows), "|---|---:|---:|",
            "| Nhắc đồ ăn / đơn hàng | %d | %.1f%% |" % (food, 100 * food / len(rows)),
            "| Đồ ăn + sự cố hoặc xử lý khiếu nại | %d | %.1f%% |" % (len(fi), 100 * len(fi) / len(rows)),
            "| … trong đó 1–2★ | %d | %.0f%% của %d |" % (sum(int(r["score"]) <= 2 for r in fi), 100 * sum(int(r["score"]) <= 2 for r in fi) / len(fi), len(fi)),
            "| Nói đúng thiếu / sai món | %d | %.1f%% |" % (strict, 100 * strict / len(rows))]
    out += ["", "## 3. Chủ đề trong %d review có sự cố" % len(fi), "", "| Chủ đề | Số review | % |", "|---|---:|---:|"]
    for k, p in TOPICS.items():
        c = sum(bool(re.search(p, r["content"], re.I)) for r in fi)
        out.append("| %s | %d | %.0f%% |" % (k, c, 100 * c / len(fi)))
    out += ["", "## 4. ShopeeFood theo tháng (review có sự cố / tổng review tháng đó)", "", "| Tháng | Có sự cố | Tổng | % |", "|---|---:|---:|---:|"]
    sf = [r for r in rows if r["app"] == "ShopeeFood"]
    m = collections.Counter(r["date"][:7] for r in sf if r["food_issue"] == "1")
    allm = collections.Counter(r["date"][:7] for r in sf)
    for k in sorted(allm)[-12:]:
        out.append("| %s | %d | %d | %.0f%% |" % (k, m[k], allm[k], 100 * m[k] / allm[k]))
    out += ["", "Tháng cuối chỉ có dữ liệu đến ngày tải nên ít review hơn."]
    with open(os.path.join(EVID, "review_stats.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
