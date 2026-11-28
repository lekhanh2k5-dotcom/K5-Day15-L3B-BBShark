"""Giao diện demo trên trình duyệt cho bản chạy thử D1 (thay cho terminal).

Chạy:  python demo/app.py      → mở http://localhost:8000
Gọi đúng hàm agent.answer() như `python run.py` — không đổi logic, không nhớ hội thoại.
Chỉ dùng thư viện chuẩn của Python.
"""
import json
import os
import re
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "codebase"))
os.chdir(ROOT)

import agent  # noqa: E402
import tracing  # noqa: E402
from ai import MODEL_NAME, MODEL_PROVIDER  # noqa: E402

ORDERS = {o["order_id"]: o for o in json.load(open(os.path.join(ROOT, "data", "mock", "orders.json"), encoding="utf-8"))["data"]}
SHOW = ["A101", "A102", "A104", "A106", "A108"]
TAG = re.compile(r"\[quyet_dinh:\s*(\w+)\s*·\s*(\d+)đ\]")

TOOL_LABEL = {
    "get_order": "Tra đơn", "get_policy": "Đọc chính sách", "get_complaint_history": "Lịch sử khiếu nại",
    "compute_remedy": "Tính bồi thường", "check_limit": "Kiểm hạn mức", "propose_refund": "Tạo đề xuất (chờ khách xác nhận)",
    "escalate_to_human": "Chuyển nhân viên",
}


def handle(text):
    tracing.begin("demo")
    try:
        out = agent.answer(text)["output"]
    finally:
        summary, events = tracing.end()
    m = TAG.search(out)
    steps = []
    for e in events:
        if e["kind"] == "model":
            steps.append({"who": "ai", "label": "AI đọc tin nhắn" if not steps or all(s["who"] != "ai" for s in steps) else "AI viết lời nhắn",
                          "detail": "%s · %s→%s token" % (e.get("model", ""), e.get("tokens_in", 0), e.get("tokens_out", 0))})
        elif e["kind"] == "tool":
            steps.append({"who": "code", "label": TOOL_LABEL.get(e["name"], e["name"]), "detail": e.get("output", "")[:160]})
        elif e["kind"] == "note":
            steps.append({"who": "note", "label": e["text"], "detail": ""})
    return {
        "reply": TAG.sub("", out).strip(),
        "action": m.group(1) if m else "", "amount": int(m.group(2)) if m else 0,
        "steps": steps, "summary": summary,
    }


PAGE = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BBShark · Hỗ trợ đơn hàng</title>
<style>
:root{--bg:#f4f1ea;--card:#fffdf8;--ink:#1d2b2c;--mute:#6b7a78;--line:#e2ddd2;--brand:#0d6b5f;--brand2:#e4f0ec;--warm:#c4532c;--ai:#5b4bd6;--ai2:#eeebff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);font:16px/1.45 "Segoe UI",system-ui,sans-serif;color:var(--ink)}
.wrap{max-width:1180px;margin:0 auto;padding:18px 16px;display:grid;grid-template-columns:270px 1fr 320px;gap:16px;height:100vh}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;display:flex;flex-direction:column;min-height:0}
h2{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin:14px 16px 8px}
.orders{overflow:auto;padding:0 10px 10px}
.order{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:0 0 8px;cursor:pointer;background:#fff}
.order:hover{border-color:var(--brand)}.order b{color:var(--brand)}.order small{color:var(--mute);display:block;font-size:13px}
.order .tag{float:right;font-size:12px;color:var(--warm)}
.chat{overflow:hidden}.head{padding:14px 18px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px}
.dot{width:36px;height:36px;border-radius:50%;background:var(--brand);color:#fff;display:grid;place-items:center;font-weight:700}
.head small{color:var(--mute);display:block;font-size:13px}
.msgs{flex:1;overflow:auto;padding:18px;display:flex;flex-direction:column;gap:12px}
.m{max-width:78%;padding:10px 14px;border-radius:14px;white-space:pre-wrap}
.me{align-self:flex-end;background:var(--brand);color:#fff;border-bottom-right-radius:4px}
.bot{align-self:flex-start;background:#fff;border:1px solid var(--line);border-bottom-left-radius:4px}
.dec{margin-top:8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.pill{font-size:13px;font-weight:600;padding:4px 10px;border-radius:99px;background:var(--brand2);color:var(--brand)}
.pill.warn{background:#fbe9e2;color:var(--warm)}.pill.ask{background:#eef1f4;color:#4a5a66}
.btn{border:0;border-radius:8px;padding:6px 12px;font-weight:600;cursor:pointer;background:var(--brand);color:#fff}
.btn:disabled{background:#9fbcb6;cursor:default}
form{display:flex;gap:8px;padding:12px;border-top:1px solid var(--line)}
input{flex:1;font:inherit;padding:11px 14px;border:1px solid var(--line);border-radius:10px;background:#fff}
input:focus{outline:2px solid var(--brand);border-color:transparent}
button.send{font:inherit;font-weight:600;padding:0 18px;border:0;border-radius:10px;background:var(--brand);color:#fff;cursor:pointer}
.typing{color:var(--mute);font-style:italic}
.steps{overflow:auto;padding:0 14px 14px}.step{display:grid;grid-template-columns:54px 1fr;gap:8px;padding:8px 0;border-bottom:1px dashed var(--line);font-size:14px}
.who{font-size:11px;font-weight:700;text-align:center;border-radius:6px;padding:3px 0;height:fit-content}
.who.ai{background:var(--ai2);color:var(--ai)}.who.code{background:var(--brand2);color:var(--brand)}.who.note{background:#f1eee6;color:var(--mute)}
.step small{display:block;color:var(--mute);font-size:12px;word-break:break-word}
.legend{font-size:13px;color:var(--mute);padding:0 16px 10px}.sum{font-size:13px;color:var(--mute);padding:8px 16px;border-top:1px solid var(--line)}
.empty{color:var(--mute);font-size:14px;padding:4px 2px}
@media(max-width:980px){.wrap{grid-template-columns:1fr;height:auto}.chat{height:70vh}}
</style></head><body>
<div class="wrap">
  <div class="card"><h2>Đơn hàng của bạn</h2><div class="legend">Bấm một đơn để điền mã vào ô chat.</div><div class="orders" id="orders"></div></div>
  <div class="card chat">
    <div class="head"><div class="dot">B</div><div><b>Hỗ trợ đơn hàng</b><small>Bản chạy thử · dữ liệu đơn là dữ liệu dựng · __MODEL__</small></div></div>
    <div class="msgs" id="msgs"><div class="m bot">Chào bạn 👋 Đơn hàng có vấn đề gì (thiếu món, sai món, giao trễ)? Bạn nhắn kèm mã đơn và tên món giúp mình nhé.</div></div>
    <form id="f"><input id="t" autocomplete="off" placeholder="Ví dụ: Đơn #A101 thiếu 1 ly trà sữa trân châu" autofocus><button class="send">Gửi</button></form>
  </div>
  <div class="card"><h2>Hệ thống đã làm gì</h2>
    <div class="legend"><span class="who ai" style="padding:2px 6px">AI</span> hiểu tin nhắn, viết lời · <span class="who code" style="padding:2px 6px">CODE</span> tra đơn, tính tiền, kiểm hạn mức</div>
    <div class="steps" id="steps"><div class="empty">Gửi một tin nhắn để xem từng bước.</div></div><div class="sum" id="sum"></div></div>
</div>
<script>
const ORDERS=__ORDERS__;
const money=n=>n.toLocaleString('vi-VN')+'đ';
const LABEL={hoan_tien:'Đề xuất hoàn tiền',voucher:'Tặng voucher',xin_loi:'Xin lỗi, chưa đủ điều kiện bù',hoi_lai:'Hỏi thêm thông tin',tu_choi:'Từ chối',chuyen_nguoi:'Chuyển nhân viên',chua_giao:'Đơn chưa giao xong'};
const od=document.getElementById('orders');
ORDERS.forEach(o=>{const late=o.delivered_min-o.promised_min;const d=document.createElement('div');d.className='order';
 d.innerHTML=`<b>${o.order_id}</b>${late>0?`<span class="tag">trễ ${late} phút</span>`:''}<small>${o.restaurant}</small>`+o.items.map(i=>`<small>${i[0]} ×${i[1]} · ${money(i[2])}</small>`).join('');
 d.onclick=()=>{const t=document.getElementById('t');t.value='Đơn #'+o.order_id+' ';t.focus()};od.appendChild(d)});
const msgs=document.getElementById('msgs'),f=document.getElementById('f'),t=document.getElementById('t');
function add(cls,html){const d=document.createElement('div');d.className='m '+cls;d.innerHTML=html;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;return d}
const esc=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
f.onsubmit=async e=>{e.preventDefault();const text=t.value.trim();if(!text)return;t.value='';add('me',esc(text));
 const w=add('bot typing','Đang kiểm tra đơn…');
 try{const r=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});const j=await r.json();
  if(j.error)throw new Error(j.error);
  const cls=j.action==='chuyen_nguoi'||j.action==='tu_choi'?'warn':(j.action==='hoi_lai'?'ask':'');
  const btn=(j.action==='hoan_tien'||j.action==='voucher')?`<button class="btn" onclick="this.disabled=true;this.textContent='Đã xác nhận ✓'">Xác nhận</button>`:'';
  w.className='m bot';w.innerHTML=esc(j.reply)+`<div class="dec"><span class="pill ${cls}">${LABEL[j.action]||j.action}${j.amount?' · '+money(j.amount):''}</span>${btn}</div>`;
  document.getElementById('steps').innerHTML=j.steps.map(s=>`<div class="step"><span class="who ${s.who}">${s.who==='ai'?'AI':s.who==='code'?'CODE':'GHI'}</span><div>${esc(s.label)}${s.detail?`<small>${esc(s.detail)}</small>`:''}</div></div>`).join('')||'<div class="empty">Không gọi công cụ (hỏi lại ngay).</div>';
  const s=j.summary;document.getElementById('sum').textContent=`Gọi model ${s.model_calls} lần · công cụ ${s.tool_calls} lần · token ${s.tokens_in}→${s.tokens_out}`;
 }catch(err){w.className='m bot';w.textContent='Lỗi: '+err.message}
 msgs.scrollTop=msgs.scrollHeight};
</script></body></html>"""


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        page = PAGE.replace("__ORDERS__", json.dumps([ORDERS[k] for k in SHOW], ensure_ascii=False)) \
                   .replace("__MODEL__", "%s · %s" % (MODEL_PROVIDER, MODEL_NAME or "mặc định"))
        self._send(200, page, "text/html")

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            text = (json.loads(self.rfile.read(n) or b"{}").get("text") or "").strip()[:1000]
            self._send(200, json.dumps(handle(text), ensure_ascii=False), "application/json")
        except Exception as e:  # noqa: BLE001
            self._send(500, json.dumps({"error": str(e)}, ensure_ascii=False), "application/json")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    url = "http://localhost:%d" % port
    print("Giao diện demo: %s  (Ctrl+C để tắt) · model: %s %s" % (url, MODEL_PROVIDER, MODEL_NAME))
    if "--no-browser" not in sys.argv:
        webbrowser.open(url)
    srv.serve_forever()
