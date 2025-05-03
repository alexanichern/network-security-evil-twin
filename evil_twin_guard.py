from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from client_guard import fingerprint_request
from mongo_db import fingerprints_collection, request_logs_collection
from datetime import datetime

class EvilTwinDetectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ip = request.client.host
        fp = fingerprint_request(request)
        status = "accepted"

        if ip in client_records and client_records[ip] != fp:
        record = await fingerprints_collection.find_one({"ip": ip})

        if record and record["fingerprint"] != fp:
            status = "blocked"
            await request_logs_collection.insert_one({
                "ip": ip,
                "fingerprint": fp,
                "timestamp": datetime.utcnow(),
                "status": status
            })
            return JSONResponse(
                content={"error": "Evil Twin detection triggered – fingerprint mismatch"},
                status_code=403
            )

        client_records[ip] = fp

        if not record:
            await fingerprints_collection.insert_one({
                "ip": ip,
                "fingerprint": fp,
                "last_seen": datetime.utcnow()
            })
        else:
            await fingerprints_collection.update_one(
                {"ip": ip},
                {"$set": {"last_seen": datetime.utcnow()}}
            )

        await request_logs_collection.insert_one({
            "ip": ip,
            "fingerprint": fp,
            "timestamp": datetime.utcnow(),
            "status": status
        })

        return await call_next(request)

