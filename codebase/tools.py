"""Công cụ của lát cắt D1 · khiếu nại đơn giao đồ ăn.

Mỗi công cụ ghi 4 ý: tên · input · output · có tác động ra ngoài không. Khớp bảng công cụ ở spec.md §4.
Dữ liệu là data GIẢ trong data/mock/ (sinh bằng data/make_mock_data.py, mô tả ở data/DATA_CARD.md).
Mọi phép tính tiền và kiểm hạn mức chạy bằng code ở đây, KHÔNG để model tự cộng trừ.
Hai công cụ có tác động (đề xuất hoàn tiền, chuyển nhân viên) chỉ tạo BẢN NHÁP, không tự thực hiện.
"""
import json
import os
from datetime import date

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK = os.path.join(ROOT, "data", "mock")
TODAY = date(2026, 11, 27)  # cố định ngày "hôm nay" của data giả để kết quả chạy lại không đổi


def _load(name):
    with open(os.path.join(MOCK, name), encoding="utf-8") as f:
        return json.load(f)["data"]


ORDERS = {o["order_id"]: o for o in _load("orders.json")}
POLICY = _load("policy.json")
COMPLAINTS = _load("complaints.json")


@tool
def get_order(order_id: str) -> dict:
    """Tra một đơn. Input: mã đơn (vd "A101"). Output: đơn {order_id, status, items[[món, sl, giá]], ship_fee,
    promised_min, delivered_min} hoặc {"error": "khong_tim_thay"}. Không tác động ra ngoài.
    Không trả số điện thoại hay địa chỉ (data giả cũng không có)."""
    o = ORDERS.get((order_id or "").strip().upper())
    return dict(o) if o else {"error": "khong_tim_thay"}


@tool
def get_policy(issue_type: str) -> dict:
    """Tra chính sách cho một loại sự cố. Input: thieu_mon | sai_mon | giao_tre.
    Output: luật {remedy, amount, max_auto…} + danh sách escalate_if, never. Không tác động ra ngoài."""
    rule = POLICY["rules"].get(issue_type)
    return {"rule": rule, "escalate_if": POLICY["escalate_if"], "never": POLICY["never"]} if rule else {"error": "khong_co_luat"}


@tool
def get_complaint_history(customer_id: str, days: int = 30) -> dict:
    """Đếm khiếu nại cũ của khách trong `days` ngày. Input: mã khách, số ngày.
    Output: {count, issues}. Không tác động ra ngoài. Chỉ dùng làm MỘT căn cứ chuyển người, không dùng để từ chối."""
    rows = [c for c in COMPLAINTS if c["customer_id"] == customer_id
            and (TODAY - date.fromisoformat(c["date"])).days <= days]
    return {"count": len(rows), "issues": [c["issue"] for c in rows]}


def _match_items(order: dict, claimed: list) -> tuple:
    """Ghép tên món khách nêu với món trong đơn (không phân biệt hoa thường, cho phép nêu một phần tên).
    Mỗi lần nêu = 1 phần; nêu quá số lượng đã đặt thì phần dư tính là "không có trong đơn"."""
    found, missing, used = [], [], {}
    for name in claimed or []:
        n = name.strip().lower()
        hit = next((it for it in order["items"] if n and (n in it[0].lower() or it[0].lower() in n)
                    and used.get(it[0], 0) < it[1]), None)
        if hit:
            used[hit[0]] = used.get(hit[0], 0) + 1
            found.append(hit)
        else:
            missing.append(name)
    return found, missing


@tool
def compute_remedy(order_id: str, issue_type: str, items: list) -> dict:
    """Tính phương án bồi thường THEO CHÍNH SÁCH, bằng code. Input: mã đơn, loại sự cố, tên các món khách nêu.
    Output: {remedy, amount, reason, items_not_in_order}. Không tác động ra ngoài.
    thieu_mon / sai_mon: mỗi món nêu tính đúng 1 phần theo giá trong đơn. giao_tre: voucher nếu trễ quá ngưỡng."""
    order = ORDERS.get(order_id)
    rule = POLICY["rules"].get(issue_type)
    if not order or not rule:
        return {"remedy": "khong_xac_dinh", "amount": 0, "reason": "thiếu đơn hoặc luật", "items_not_in_order": []}
    if issue_type == "giao_tre":
        if order["delivered_min"] is None:
            return {"remedy": "chua_giao", "amount": 0, "reason": "đơn chưa giao xong", "items_not_in_order": []}
        late = order["delivered_min"] - order["promised_min"]
        if late > rule["late_threshold_min"]:
            return {"remedy": "voucher", "amount": rule["voucher"], "reason": "trễ %d phút > %d" % (late, rule["late_threshold_min"]),
                    "items_not_in_order": []}
        return {"remedy": "xin_loi", "amount": 0, "reason": "trễ %d phút, chưa quá %d" % (max(late, 0), rule["late_threshold_min"]),
                "items_not_in_order": []}
    found, missing = _match_items(order, items)
    amount = sum(it[2] for it in found)
    return {"remedy": "hoan_tien" if found else "khong_xac_dinh", "amount": amount,
            "reason": "giá món trong đơn: " + ", ".join("%s %dđ" % (it[0], it[2]) for it in found),
            "items_not_in_order": missing}


@tool
def check_limit(issue_type: str, amount: int) -> dict:
    """Kiểm số tiền có nằm trong hạn mức tự xử lý không — bằng code. Input: loại sự cố, số tiền.
    Output: {within: bool, max_auto}. Không tác động ra ngoài."""
    rule = POLICY["rules"].get(issue_type) or {}
    cap = rule.get("max_auto", rule.get("voucher", 0))
    return {"within": amount <= cap, "max_auto": cap}


@tool
def propose_refund(order_id: str, amount: int, kind: str) -> dict:
    """Tạo ĐỀ XUẤT bồi thường để khách bấm xác nhận. Input: mã đơn, số tiền, hoan_tien | voucher.
    Output: bản nháp {status: "cho_khach_xac_nhan"}. TÁC ĐỘNG: chưa — tiền chỉ đi khi khách xác nhận (bản chạy thử không chuyển tiền)."""
    return {"order_id": order_id, "amount": amount, "kind": kind, "status": "cho_khach_xac_nhan"}


@tool
def escalate_to_human(order_id: str, reason: str) -> dict:
    """Chuyển ca cho nhân viên. Input: mã đơn (có thể rỗng), lý do. Output: phiếu {ticket, status: "cho_nhan_vien"}.
    TÁC ĐỘNG: có, nhưng đảo được (nhân viên có thể trả ca lại). Bản chạy thử chỉ ghi phiếu, không gửi đi đâu."""
    return {"ticket": "T-%s" % (order_id or "NA"), "reason": reason, "status": "cho_nhan_vien"}
