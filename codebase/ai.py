"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

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

Hỗ trợ các nhà cung cấp bằng thư viện chuẩn Python (urllib, không cần cài SDK):
    gemini · openrouter · openai · groq · anthropic · ollama (và openai_compatible qua API_BASE_URL).
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False   # đổi thành True để in nguyên phản hồi API khi cần debug tên trường
TEMPERATURE = 0    # 0 để kết quả chạy lại ổn định nhất có thể

OPENAI_COMPATIBLE = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
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


def call_openai_compatible(url: str, system: str, user: str) -> dict:
    """OpenRouter / OpenAI / Groq (cùng chuẩn chat completions). Token lấy từ trường usage."""
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(
        url,
        {"Authorization": "Bearer " + API_KEY},
        {"model": MODEL_NAME, "temperature": TEMPERATURE, "messages": messages},
    )
    usage = data.get("usage") or {}
    return {
        "text": data["choices"][0]["message"]["content"] or "",
        "tokens_in": usage.get("prompt_tokens", 0),
        "tokens_out": usage.get("completion_tokens", 0),
    }


def call_gemini(system: str, user: str) -> dict:
    """Google Gemini (generativelanguage API). Token lấy từ usageMetadata (gồm cả token suy nghĩ nếu có)."""
    url = API_BASE_URL or ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL_NAME)
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": TEMPERATURE},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {"x-goog-api-key": API_KEY}, body)
    parts = ((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
    meta = data.get("usageMetadata") or {}
    return {
        "text": "".join(p.get("text", "") for p in parts if isinstance(p, dict)),
        "tokens_in": meta.get("promptTokenCount", 0),
        "tokens_out": meta.get("candidatesTokenCount", 0) + meta.get("thoughtsTokenCount", 0),
    }


def call_claude(system: str, user: str) -> dict:
    """Anthropic Claude (Messages API). Token lấy từ trường usage."""
    url = API_BASE_URL or "https://api.anthropic.com/v1/messages"
    data = post_json(
        url,
        {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        {
            "model": MODEL_NAME,
            "max_tokens": 1024,
            "temperature": TEMPERATURE,
            "system": system or "",
            "messages": [{"role": "user", "content": user}],
        },
    )
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    usage = data.get("usage") or {}
    return {
        "text": text,
        "tokens_in": usage.get("input_tokens", 0),
        "tokens_out": usage.get("output_tokens", 0),
    }


def call_ollama(system: str, user: str) -> dict:
    """Ollama chạy local. Token lấy từ prompt_eval_count / eval_count."""
    url = API_BASE_URL or "http://localhost:11434/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(
        url,
        {},
        {"model": MODEL_NAME, "messages": messages, "stream": False, "options": {"temperature": TEMPERATURE}},
        timeout=300,
    )
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
        raise NotImplementedError("điền MODEL_NAME trong .env (xem .env.example)")
    if MODEL_PROVIDER != "ollama" and not API_KEY:
        raise NotImplementedError("điền API_KEY trong .env (xem .env.example)")

    if MODEL_PROVIDER in ("gemini", "google"):
        r = call_gemini(system, user)
    elif MODEL_PROVIDER in OPENAI_COMPATIBLE:
        r = call_openai_compatible(API_BASE_URL or OPENAI_COMPATIBLE[MODEL_PROVIDER], system, user)
    elif MODEL_PROVIDER == "openai_compatible" and API_BASE_URL:
        r = call_openai_compatible(API_BASE_URL, system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        supported = ", ".join(["gemini", *OPENAI_COMPATIBLE.keys(), "anthropic", "ollama"])
        raise NotImplementedError("MODEL_PROVIDER=%s chưa hỗ trợ — dùng một trong: %s" % (MODEL_PROVIDER, supported))

    return {
        "text": r["text"],
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
