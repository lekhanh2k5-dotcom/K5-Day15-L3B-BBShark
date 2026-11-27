"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False   # đổi thành True để in nguyên phản hồi API khi cần debug tên trường
TEMPERATURE = 0    # 0 để kết quả chạy lại ổn định nhất có thể

# Nhà cung cấp dùng chuẩn chat completions của OpenAI (cùng hàm _call_openai, khác địa chỉ)
OPENAI_COMPATIBLE = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
}


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
API_BASE_URL = (os.environ.get("API_BASE_URL") or "").strip()


def post_json(url: str, headers: dict, body: dict, timeout: int = 60) -> dict:
    """Gửi POST JSON bằng thư viện chuẩn (urllib), trả về dict phản hồi."""
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def _call_openai(system: str, user: str, url: str = "") -> dict:
    url = API_BASE_URL or url or OPENAI_COMPATIBLE["openai"]
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(
        url,
        {"Authorization": "Bearer " + API_KEY},
        {"model": MODEL_NAME, "messages": messages, "temperature": TEMPERATURE},
    )
    usage = data["usage"]
    return {
        "text": data["choices"][0]["message"]["content"] or "",
        "tokens_in": usage["prompt_tokens"],
        "tokens_out": usage["completion_tokens"],
    }


def _call_claude(system: str, user: str) -> dict:
    url = API_BASE_URL or "https://api.anthropic.com/v1/messages"
    data = post_json(
        url,
        {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        {
            "model": MODEL_NAME,
            "max_tokens": 1024,
            "system": system or "",
            "messages": [{"role": "user", "content": user}],
        },
    )
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    usage = data["usage"]
    return {
        "text": text,
        "tokens_in": usage["input_tokens"],
        "tokens_out": usage["output_tokens"],
    }


def _call_gemini(system: str, user: str) -> dict:
    base = API_BASE_URL or f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
    sep = "&" if "?" in base else "?"
    url = f"{base}{sep}key={urllib.parse.quote(API_KEY)}"
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}], "generationConfig": {"temperature": TEMPERATURE}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {}, body)
    candidates = data.get("candidates") or []
    parts = (candidates[0].get("content") or {}).get("parts", []) if candidates else []
    text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
    usage = data.get("usageMetadata") or {}
    tokens_in = int(usage.get("promptTokenCount", 0))
    tokens_out = int(usage.get("candidatesTokenCount", 0)) + int(usage.get("thoughtsTokenCount", 0))
    return {
        "text": text,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
    }


def _call_ollama(system: str, user: str) -> dict:
    url = API_BASE_URL or "http://localhost:11434/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {
        "text": data["message"]["content"] or "",
        "tokens_in": data.get("prompt_eval_count", 0),
        "tokens_out": data.get("eval_count", 0),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong file .env")
    if MODEL_PROVIDER != "ollama" and not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong file .env cho MODEL_PROVIDER=%s" % MODEL_PROVIDER)

    if MODEL_PROVIDER in OPENAI_COMPATIBLE:
        r = _call_openai(system, user, OPENAI_COMPATIBLE[MODEL_PROVIDER])
    elif MODEL_PROVIDER == "openai_compatible":
        r = _call_openai(system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        r = _call_claude(system, user)
    elif MODEL_PROVIDER in ("gemini", "google"):
        r = _call_gemini(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = _call_ollama(system, user)
    else:
        raise NotImplementedError(
            "Không hỗ trợ MODEL_PROVIDER=%s trong codebase/ai.py (hỗ trợ: openai, openrouter, groq, openai_compatible, anthropic, gemini, ollama)"
            % MODEL_PROVIDER
        )

    return {
        "text": r["text"],
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
