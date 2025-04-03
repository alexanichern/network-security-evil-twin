from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from client_guard import fingerprint_request

client_records = {}  # Stores IP → fingerprint

class EvilTwinDetectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ip = request.client.host
        fp = fingerprint_request(request)

        # If we’ve seen the IP before but the fingerprint changed
        if ip in client_records and client_records[ip] != fp:
            return JSONResponse(
                content={"error": "Evil Twin detection triggered – fingerprint mismatch"},
                status_code=403
            )

        # Record it if it’s new or still matches
        client_records[ip] = fp
        return await call_next(request)
