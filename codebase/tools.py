"""Công cụ của bài toán Track D1 (Khiếu nại đơn giao đồ ăn thiếu món).

Mỗi công cụ là một hàm Python có @tool với docstring đủ 4 ý (khớp spec.md §4):
    tên · input · output · có tác động ra ngoài không.
Các công cụ có tác động tài chính / vận hành (hoàn tiền, chuyển CSKH) KHÔNG tự thực thi
mà chỉ tạo bản nháp chờ khách xác nhận và nhân viên duyệt.
"""
import json
import os
import re
import unicodedata
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
ORDERS_PATH = os.path.join(ROOT, "data", "orders.json")
POLICY_PATH = os.path.join(ROOT, "data", "policy.json")


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _normalize(text: str) -> str:
    """Chuẩn hoá chữ thường, bỏ dấu tiếng Việt để so khớp tên món linh hoạt."""
    s = unicodedata.normalize("NFD", (text or "").lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.replace("đ", "d")
    return re.sub(r"\s+", " ", s).strip()


def _find_order(order_id: str) -> dict:
    clean_id = (order_id or "").strip().lstrip("#").upper()
    if not clean_id:
        return {"found": False, "order": None, "message": "Chưa cung cấp mã đơn hàng."}
    data = _load_json(ORDERS_PATH)
    for order in data.get("orders", []):
        if order.get("order_id", "").upper() == clean_id:
            return {"found": True, "order": order, "message": f"Tìm thấy đơn {clean_id}."}
    return {"found": False, "order": None, "message": f"Không tìm thấy đơn hàng {clean_id} trong hệ thống."}


def _evaluate_eligibility(order_id: str, missing_item_name: str, missing_qty: int = 1) -> dict:
    order_res = _find_order(order_id)
    if not order_res["found"]:
        return {
            "eligible": False,
            "action": "ask_clarification",
            "refund_amount_vnd": 0,
            "matched_item": None,
            "violated_rules": [],
            "reason": order_res["message"],
        }

    order = order_res["order"]
    policy = _load_json(POLICY_PATH)
    limits = policy.get("limits", {})

    if order.get("status") != limits.get("eligible_order_status", "delivered"):
        return {
            "eligible": False,
            "action": "escalate",
            "refund_amount_vnd": 0,
            "matched_item": None,
            "violated_rules": ["CS-01"],
            "reason": f"Đơn {order['order_id']} đang ở trạng thái '{order.get('status')}', chưa hoàn tất giao hàng (CS-01).",
        }

    hours = order.get("hours_since_delivered")
    max_hours = limits.get("complaint_window_hours", 24)
    if hours is None or hours > max_hours:
        return {
            "eligible": False,
            "action": "escalate",
            "refund_amount_vnd": 0,
            "matched_item": None,
            "violated_rules": ["CS-02"],
            "reason": f"Đơn {order['order_id']} đã giao quá thời hạn khiếu nại {max_hours} giờ ({hours} giờ) (CS-02).",
        }

    recent_claims = order.get("customer_recent_claims_30d", 0)
    max_claims = limits.get("max_recent_claims_30d", 2)
    if recent_claims > max_claims:
        return {
            "eligible": False,
            "action": "escalate",
            "refund_amount_vnd": 0,
            "matched_item": None,
            "violated_rules": ["CS-05"],
            "reason": f"Tài khoản đã có {recent_claims} lần khiếu nại trong 30 ngày gần nhất (vượt ngưỡng {max_claims}) — cần CSKH kiểm tra (CS-05).",
        }

    target_norm = _normalize(missing_item_name)
    matched_item = None
    if target_norm:
        for item in order.get("items", []):
            item_norm = _normalize(item.get("name", ""))
            if target_norm in item_norm or item_norm in target_norm:
                matched_item = item
                break

    if not matched_item:
        available = ", ".join(f"{it['name']} ({it['unit_price_vnd']:,}đ)" for it in order.get("items", []))
        return {
            "eligible": False,
            "action": "ask_clarification",
            "refund_amount_vnd": 0,
            "matched_item": None,
            "violated_rules": [],
            "reason": f"Không khớp món '{missing_item_name}' trong đơn {order['order_id']}. Các món trong đơn: {available}.",
        }

    qty = max(1, int(missing_qty))
    ordered_qty = int(matched_item.get("qty", 1))
    if qty > ordered_qty:
        return {
            "eligible": False,
            "action": "ask_clarification",
            "refund_amount_vnd": 0,
            "matched_item": matched_item,
            "violated_rules": ["CS-04"],
            "reason": f"Số lượng báo thiếu ({qty}) vượt số lượng đã đặt ({ordered_qty}) của món '{matched_item['name']}'.",
        }

    refund_amount = qty * int(matched_item.get("unit_price_vnd", 0))
    limit_vnd = int(limits.get("auto_propose_limit_vnd", 100000))
    max_qty = int(limits.get("max_missing_qty_auto", 2))

    if refund_amount > limit_vnd or qty > max_qty:
        return {
            "eligible": False,
            "action": "escalate",
            "refund_amount_vnd": refund_amount,
            "matched_item": matched_item,
            "violated_rules": ["CS-03"],
            "reason": (
                f"Giá trị phần thiếu ({refund_amount:,}đ, SL {qty}) vượt hạn mức đề xuất tự động "
                f"({limit_vnd:,}đ / tối đa {max_qty} phần) — cần chuyển nhân viên CSKH (CS-03)."
            ),
        }

    return {
        "eligible": True,
        "action": "propose_refund",
        "refund_amount_vnd": refund_amount,
        "matched_item": matched_item,
        "violated_rules": [],
        "reason": f"Đủ điều kiện đề xuất hoàn {refund_amount:,}đ cho {qty}x '{matched_item['name']}' theo CS-01, CS-02, CS-03, CS-04.",
    }


@tool
def lookup_order(order_id: str) -> dict:
    """lookup_order · Input: order_id (str, vd 'DH1001').
    Output: dict {'found': bool, 'order': dict | None, 'message': str}.
    Tác động ra ngoài: Không (chỉ đọc data/orders.json)."""
    return _find_order(order_id)


@tool
def get_refund_policy(rule_code: str = "") -> dict:
    """get_refund_policy · Input: rule_code (str, để trống để lấy toàn bộ chính sách hoặc truyền mã 'CS-01'..'CS-06').
    Output: dict chứa limits và danh sách rules từ data/policy.json.
    Tác động ra ngoài: Không (chỉ đọc data/policy.json)."""
    policy = _load_json(POLICY_PATH)
    code = (rule_code or "").strip().upper()
    if code:
        matched = [r for r in policy.get("rules", []) if r.get("code", "").upper() == code]
        return {"version": policy.get("version"), "limits": policy.get("limits", {}), "rules": matched}
    return policy


@tool
def check_refund_eligibility(order_id: str, missing_item_name: str, missing_qty: int = 1) -> dict:
    """check_refund_eligibility · Input: order_id (str), missing_item_name (str), missing_qty (int >= 1).
    Output: dict kết quả kiểm tra bằng CODE gồm eligible (bool), action ('propose_refund' | 'escalate' | 'ask_clarification'),
    refund_amount_vnd (int), matched_item (dict | None), violated_rules (list[str]), reason (str).
    Tác động ra ngoài: Không (chỉ tính toán và kiểm tra hạn mức theo data/orders.json và data/policy.json)."""
    return _evaluate_eligibility(order_id, missing_item_name, missing_qty)


@tool
def create_refund_draft(order_id: str, item_name: str, missing_qty: int = 1) -> dict:
    """create_refund_draft · Input: order_id (str), item_name (str), missing_qty (int >= 1).
    Output: dict bản nháp đề xuất hoàn tiền (chỉ tạo khi qua kiểm tra hạn mức bằng code).
    Tác động ra ngoài: Có tác động tài chính nếu thực thi → KHÔNG tự hoàn tiền, CHỈ trả về bản nháp trạng thái CHO_KHACH_XAC_NHAN_VA_DUYET."""
    check = _evaluate_eligibility(order_id, item_name, missing_qty)
    if not check["eligible"]:
        return {
            "created": False,
            "status": "TU_CHOI_TAO_NHAP",
            "reason": check["reason"],
            "violated_rules": check["violated_rules"],
        }

    item = check["matched_item"]
    return {
        "created": True,
        "draft_id": f"DRAFT-RF-{order_id.upper().lstrip('#')}-{item['item_id']}",
        "status": "CHO_KHACH_XAC_NHAN_VA_DUYET",
        "order_id": order_id.upper().lstrip("#"),
        "item_name": item["name"],
        "missing_qty": missing_qty,
        "refund_amount_vnd": check["refund_amount_vnd"],
        "policy_codes": ["CS-01", "CS-02", "CS-03", "CS-04"],
        "note": "Bản nháp đề xuất hoàn tiền. Chưa chuyển tiền và chưa đóng khiếu nại; cần khách xác nhận và nhân viên/hệ thống duyệt.",
    }


@tool
def create_escalation_ticket(order_id: str, reason_code: str, summary: str) -> dict:
    """create_escalation_ticket · Input: order_id (str, có thể trống nếu chưa có mã đơn), reason_code (str, vd 'CS-03'), summary (str).
    Output: dict bản nháp phiếu chuyển nhân viên CSKH.
    Tác động ra ngoài: Có tác động vận hành nếu gửi thật → CHỈ trả về bản nháp phiếu trạng thái CHO_CHUYEN_CSKH."""
    clean_id = (order_id or "KHONG_RO").strip().lstrip("#").upper()
    return {
        "created": True,
        "ticket_id": f"ESC-{clean_id}-{reason_code.upper() or 'GEN'}",
        "status": "CHO_CHUYEN_CSKH",
        "order_id": clean_id,
        "reason_code": reason_code or "CS-06",
        "summary": summary[:200],
        "note": "Bản nháp phiếu chuyển nhân viên CSKH xử lý thủ công.",
    }
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
