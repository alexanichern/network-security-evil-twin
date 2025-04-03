import uvicorn
from fastapi.responses import JSONResponse
from app import app
from rate_limiter import createEndPoint
from evil_twin_guard import EvilTwinDetectionMiddleware

# Add the Evil Twin protection middleware
app.add_middleware(EvilTwinDetectionMiddleware)

# Test endpoint
async def testFunction():
    return JSONResponse(content={"response": "i see you"}, status_code=200)

# Create protected endpoints
createEndPoint("/test", ["GET"], 10, testFunction)
createEndPoint("/foo", ["GET"], 30, testFunction)

# Run server
uvicorn.run(app, host="127.0.0.1", port=10000)

