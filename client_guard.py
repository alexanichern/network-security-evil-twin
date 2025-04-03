from fastapi import Request
import hashlib

def fingerprint_request(request: Request):
    user_agent = request.headers.get("user-agent", "")
    accept_lang = request.headers.get("accept-language", "")
    encoding = request.headers.get("accept-encoding", "")
    referer = request.headers.get("referer", "")
    raw_fp = f"{user_agent}|{accept_lang}|{encoding}|{referer}"
    return hashlib.sha256(raw_fp.encode()).hexdigest()
