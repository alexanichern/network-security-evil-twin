from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.evil_twin_db
fingerprints_collection = database.get_collection("fingerprints")
request_logs_collection = database.get_collection("request_logs")

