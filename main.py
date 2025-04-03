import uvicorn
from fastapi.responses import JSONResponse
from app import app
from rate_limiter import createEndPoint
from evil_twin_guard import EvilTwinDetectionMiddleware

app.add_middleware(EvilTwinDetectionMiddleware)

async def testFunction():
    return JSONResponse(content={"response": "i see you"}, status_code=200)

createEndPoint("/test", ["GET"], 10, testFunction)
createEndPoint("/foo", ["GET"], 30, testFunction)

uvicorn.run(app, host="127.0.0.1", port=10000)
