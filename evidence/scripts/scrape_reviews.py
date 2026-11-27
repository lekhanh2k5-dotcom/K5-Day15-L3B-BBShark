"""Cào review công khai trên Google Play của app giao đồ ăn, lọc theo từ khoá, rút mẫu để gán nhãn tay.

Cách đếm được viết TRƯỚC trong evidence/data-mining.md §1. Script chỉ làm đúng các bước ở đó.

Chạy:
    pip install google-play-scraper
    python evidence/scripts/scrape_reviews.py

Ra file:
    evidence/raw-reviews.csv      toàn bộ review đã tải (KHÔNG commit, .gitignore chặn evidence/**/raw-*)
    evidence/review_counts.csv    số đếm theo từng app (commit)
    evidence/label_sample.csv     100 review ShopeeFood rút ngẫu nhiên (seed 42) để gán nhãn tay (commit)

Không lưu tên người viết, ảnh đại diện hay mã người dùng: chỉ giữ mã review rút gọn (băm), app, ngày, số sao, nội dung.
Review mới được đăng liên tục, nên chạy lại vào ngày khác sẽ ra tập hơi khác: ngày tải ghi trong review_counts.csv.
"""
import csv
import datetime as dt
import hashlib
import os
import random
import re
import sys

from google_play_scraper import Sort, reviews

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
EVID = os.path.dirname(HERE)

# app → (mã Google Play, số review mới nhất cần tải)
APPS = {
    "ShopeeFood": ("com.deliverynow", 10000),
    "Grab": ("com.grabtaxi.passenger", 3000),
    "be": ("xyz.be.customer", 3000),
    "XanhSM": ("com.gsm.customer", 3000),
}
SAMPLE_APP, SAMPLE_N, SEED = "ShopeeFood", 100, 42

# Bước lọc 1: review có nhắc tới đồ ăn / đơn hàng
FOOD = re.compile(r"đồ ăn|do an|món|quán|food|đơn hàng|don hang|đơn|giao hàng", re.I)
# Bước lọc 2: review có nhắc tới một sự cố của đơn hoặc việc xử lý khiếu nại
ISSUE = re.compile(
    r"thiếu|thieu|sai món|giao nhầm|nhầm món|trễ|chậm|cham|nguội|đổ|hoàn tiền|hoan tien|hoàn lại|"
    r"khiếu nại|khieu nai|hủy đơn|huỷ đơn|bồi thường|hỗ trợ|ho tro|chăm sóc|tổng đài|chatbot|chat bot",
    re.I,
)
# Đếm chặt (đúng lát cắt D1): review nói đơn bị thiếu món / sai món
STRICT = re.compile(r"thiếu món|thiếu đồ|giao thiếu|làm thiếu|sai món|nhầm món|giao nhầm|giao sai", re.I)


def short_id(review_id: str) -> str:
    return hashlib.sha1(review_id.encode("utf-8")).hexdigest()[:10]


def main() -> int:
    today = dt.date.today().isoformat()
    raw_rows, count_rows = [], []
    for app, (pid, n) in APPS.items():
        rs, _ = reviews(pid, lang="vi", country="vn", sort=Sort.NEWEST, count=n)
        food = issue = low = strict = 0
        for r in rs:
            text = (r.get("content") or "").replace("\r", " ").replace("\n", " ").strip()
            is_food = bool(FOOD.search(text))
            is_issue = is_food and bool(ISSUE.search(text))
            food += is_food
            issue += is_issue
            low += is_issue and r["score"] <= 2
            is_strict = bool(STRICT.search(text))
            strict += is_strict
            raw_rows.append({
                "id": short_id(r["reviewId"]), "app": app, "date": r["at"].date().isoformat(),
                "score": r["score"], "food": int(is_food), "food_issue": int(is_issue), "thieu_sai_mon": int(is_strict), "content": text,
            })
        dates = [r["at"].date() for r in rs]
        count_rows.append({
            "app": app, "package": pid, "fetched_on": today, "N": len(rs),
            "from": min(dates).isoformat() if dates else "", "to": max(dates).isoformat() if dates else "",
            "food": food, "food_issue": issue, "food_issue_le2star": low, "thieu_sai_mon": strict,
        })
        print("%-10s N=%5d  đồ ăn/đơn=%4d  đồ ăn+sự cố=%4d  (≤2★: %d)  thiếu/sai món=%d" % (app, len(rs), food, issue, low, strict))

    with open(os.path.join(EVID, "raw-reviews.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(raw_rows[0]))
        w.writeheader()
        w.writerows(raw_rows)
    with open(os.path.join(EVID, "review_counts.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(count_rows[0]))
        w.writeheader()
        w.writerows(count_rows)

    pool = sorted((r for r in raw_rows if r["app"] == SAMPLE_APP and r["food_issue"]), key=lambda r: r["id"])
    sample = random.Random(SEED).sample(pool, min(SAMPLE_N, len(pool)))
    with open(os.path.join(EVID, "label_sample.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stt", "id", "app", "date", "score", "content", "label", "nguoi_gan", "ghi_chu"])
        for i, r in enumerate(sample, 1):
            w.writerow([i, r["id"], r["app"], r["date"], r["score"], r["content"], "", "", ""])
    print("Mẫu gán nhãn: %d/%d review %s (seed %d) → evidence/label_sample.csv" % (len(sample), len(pool), SAMPLE_APP, SEED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
