from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from client_guard import fingerprint_request
from datetime import datetime
from database import get_connection

client_records = {}

class EvilTwinDetectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ip = request.client.host
        fp = fingerprint_request(request)
        status = "accepted"

        if ip in client_records and client_records[ip] != fp:
            status = "blocked"
            self.log(ip, fp, status)
            return JSONResponse({"error": "Fingerprint mismatch"}, status_code=403)

        client_records[ip] = fp
        stat = "accepted"
        self.log(ip, fp, status)
        return await call_next(request)

    def log(self, ip, fp, status):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO RequestLogs (ip, fingerprint, timestamp, status) VALUES (%s, %s, %s, %s)",
            (ip, fp, datetime.utcnow(), status)
        )
        conn.commit()
        cur.close()
        conn.close()

