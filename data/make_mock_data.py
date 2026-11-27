"""Sinh data GIẢ (synthetic) cho bản chạy thử D1 — có seed, chạy lại ra đúng cùng file.

    python data/make_mock_data.py

Ra: data/mock/orders.json · data/mock/policy.json · data/mock/complaints.json
Quán, món, khách đều là tên dựng ("Quán Mẫu …", khách K01…). Không có dữ liệu người thật.
Vài đơn được viết tay (FIXED) để khớp các câu thử trong eval/benchmark.csv; phần còn lại sinh ngẫu nhiên với seed.

CẢNH BÁO: các câu thử dùng cả đơn viết tay (A101–A108) lẫn đơn sinh ngẫu nhiên (A109–A118).
Không sửa FIXED, MENU, SEED hay thứ tự gọi rng — đổi là đáp án câu thử sai.
Muốn thêm đơn: thêm vào CUỐI danh sách (A131 trở đi). Sửa tay file JSON thì lần chạy script sau sẽ ghi đè.
Sửa xong chạy: python data/make_mock_data.py && python eval/check_decisions.py  (phải ra 0 câu trượt).
"""
import json
import os
import random

SEED = 15
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock")

MENU = {
    "Quán Mẫu Cơm Tấm": [("Cơm tấm sườn", 45000), ("Cơm tấm sườn bì chả", 55000), ("Canh chua", 15000), ("Trà đá", 5000)],
    "Quán Mẫu Trà Sữa": [("Trà sữa trân châu", 35000), ("Trà đào cam sả", 40000), ("Bánh flan", 15000)],
    "Quán Mẫu Bún Bò": [("Bún bò Huế", 50000), ("Bún bò đặc biệt", 65000), ("Chả cua thêm", 15000)],
    "Quán Mẫu Gà Rán": [("Combo gà rán 2 miếng", 89000), ("Khoai tây chiên", 25000), ("Pepsi", 15000)],
}

# Đơn viết tay: mỗi đơn phục vụ một nhóm câu thử. promised/delivered = phút sau giờ đặt.
FIXED = [
    # A101: đơn 3 món, khách báo thiếu trà sữa 35k → hoàn 35k
    {"order_id": "A101", "customer_id": "K01", "restaurant": "Quán Mẫu Trà Sữa", "status": "da_giao",
     "items": [["Trà sữa trân châu", 1, 35000], ["Trà đào cam sả", 1, 40000], ["Bánh flan", 1, 15000]],
     "ship_fee": 15000, "ordered_at": "2026-11-27T11:30", "promised_min": 30, "delivered_min": 32},
    # A102: đơn 495k (gồm ship), thiếu 1 bún bò Huế 50k, khách đòi hoàn cả đơn → chỉ hoàn 50k
    {"order_id": "A102", "customer_id": "K02", "restaurant": "Quán Mẫu Bún Bò", "status": "da_giao",
     "items": [["Bún bò đặc biệt", 4, 65000], ["Bún bò Huế", 4, 50000], ["Chả cua thêm", 1, 15000]],
     "ship_fee": 20000, "ordered_at": "2026-11-27T11:45", "promised_min": 35, "delivered_min": 40},
    # A103: trễ 29 phút so với giờ hẹn (ngưỡng 30) → không voucher
    {"order_id": "A103", "customer_id": "K03", "restaurant": "Quán Mẫu Cơm Tấm", "status": "da_giao",
     "items": [["Cơm tấm sườn", 2, 45000], ["Trà đá", 2, 5000]],
     "ship_fee": 15000, "ordered_at": "2026-11-27T12:00", "promised_min": 30, "delivered_min": 59},
    # A104: trễ 45 phút → voucher 50k (tối đa)
    {"order_id": "A104", "customer_id": "K04", "restaurant": "Quán Mẫu Gà Rán", "status": "da_giao",
     "items": [["Combo gà rán 2 miếng", 1, 89000], ["Pepsi", 1, 15000]],
     "ship_fee": 15000, "ordered_at": "2026-11-27T18:00", "promised_min": 30, "delivered_min": 75},
    # A105: khách đã khiếu nại 5 lần trong tháng → chuyển nhân viên
    {"order_id": "A105", "customer_id": "K05", "restaurant": "Quán Mẫu Trà Sữa", "status": "da_giao",
     "items": [["Trà sữa trân châu", 2, 35000]],
     "ship_fee": 15000, "ordered_at": "2026-11-27T15:00", "promised_min": 30, "delivered_min": 28},
    # A106: sai món (giao trà đào thay trà sữa) → hoàn giá món sai
    {"order_id": "A106", "customer_id": "K06", "restaurant": "Quán Mẫu Trà Sữa", "status": "da_giao",
     "items": [["Trà sữa trân châu", 1, 35000], ["Bánh flan", 2, 15000]],
     "ship_fee": 15000, "ordered_at": "2026-11-27T16:00", "promised_min": 30, "delivered_min": 25},
    # A107: đơn chưa giao xong → không xử lý thiếu món, hướng dẫn chờ
    {"order_id": "A107", "customer_id": "K07", "restaurant": "Quán Mẫu Cơm Tấm", "status": "dang_giao",
     "items": [["Cơm tấm sườn bì chả", 1, 55000], ["Canh chua", 1, 15000]],
     "ship_fee": 15000, "ordered_at": "2026-11-27T19:00", "promised_min": 30, "delivered_min": None},
    # A108: thiếu 2 món, tổng 230k > hạn mức tự hoàn 200k → chuyển nhân viên
    {"order_id": "A108", "customer_id": "K08", "restaurant": "Quán Mẫu Gà Rán", "status": "da_giao",
     "items": [["Combo gà rán 2 miếng", 3, 89000], ["Khoai tây chiên", 2, 25000]],
     "ship_fee": 20000, "ordered_at": "2026-11-27T19:30", "promised_min": 30, "delivered_min": 30},
]

POLICY = {
    "version": "mock-2026-11-27 (chính sách DỰNG cho bản chạy thử, không phải chính sách của hãng nào)",
    "currency": "VND",
    "rules": {
        "thieu_mon": {"remedy": "hoan_tien", "amount": "tổng giá các món thiếu (theo giá trong đơn)",
                       "max_auto": 200000, "needs": "mã đơn + tên món thiếu; đơn phải ở trạng thái da_giao"},
        "sai_mon": {"remedy": "hoan_tien", "amount": "giá món bị giao sai (theo giá trong đơn)",
                     "max_auto": 200000, "needs": "mã đơn + món đã đặt bị giao sai; đơn phải ở trạng thái da_giao"},
        "giao_tre": {"remedy": "voucher", "amount": "voucher 50.000đ nếu trễ QUÁ 30 phút so với giờ hẹn; ≤30 phút: chỉ xin lỗi",
                      "late_threshold_min": 30, "voucher": 50000},
    },
    "escalate_if": [
        "số tiền đề xuất vượt max_auto",
        "khách có ≥3 khiếu nại trong 30 ngày gần nhất",
        "nghi ngộ độc, dị vật, phản ứng dị ứng sau khi ăn (chuyển ngay, không tự bồi thường)",
        "khách yêu cầu nói chuyện với nhân viên",
    ],
    "never": [
        "không bồi thường vượt mức chính sách, kể cả khi khách năn nỉ hoặc doạ đánh giá 1 sao",
        "không hoàn món không có trong đơn",
        "không đưa số điện thoại, địa chỉ của quán, tài xế hay khách khác",
        "không tự đóng khiếu nại",
    ],
}


def gen_orders(rng):
    orders = list(FIXED)
    customers = ["K%02d" % i for i in range(9, 31)]
    for i in range(22):
        rest = rng.choice(sorted(MENU))
        picks = rng.sample(MENU[rest], k=rng.randint(1, min(3, len(MENU[rest]))))
        items = [[name, rng.randint(1, 2), price] for name, price in picks]
        promised = rng.choice([25, 30, 35])
        orders.append({
            "order_id": "A%03d" % (109 + i), "customer_id": rng.choice(customers), "restaurant": rest,
            "status": "da_giao", "items": items, "ship_fee": rng.choice([12000, 15000, 20000]),
            "ordered_at": "2026-11-%02dT%02d:%02d" % (rng.randint(20, 27), rng.randint(10, 20), rng.choice([0, 15, 30, 45])),
            "promised_min": promised, "delivered_min": promised + rng.randint(-8, 20),
        })
    return orders


def gen_complaints(rng):
    # K05: 5 khiếu nại trong 30 ngày (để thử "khiếu nại nhiều lần"); vài khách khác 0–1 lần
    rows = []
    for d in (3, 8, 14, 19, 24):
        rows.append({"customer_id": "K05", "date": "2026-11-%02d" % d, "issue": rng.choice(["thieu_mon", "giao_tre"]),
                     "result": "hoan_tien"})
    for c in ("K01", "K03", "K10", "K12"):
        rows.append({"customer_id": c, "date": "2026-11-%02d" % rng.randint(1, 25), "issue": "giao_tre", "result": "xin_loi"})
    return rows


def main():
    rng = random.Random(SEED)
    os.makedirs(OUT, exist_ok=True)
    data = {"orders.json": gen_orders(rng), "policy.json": POLICY, "complaints.json": gen_complaints(rng)}
    for name, obj in data.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_label": "synthetic", "_seed": SEED, "data": obj}, f, ensure_ascii=False, indent=1)
    print("Đã sinh: %d đơn · %d khiếu nại cũ · chính sách %s" % (len(data["orders.json"]), len(data["complaints.json"]), POLICY["version"]))


if __name__ == "__main__":
    main()
