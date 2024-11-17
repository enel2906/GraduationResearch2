from polygon.rest import RESTClient
import pymongo
import json
import config
from datetime import datetime

client = RESTClient(config.API_KEY)

# MongoDB Connection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["stock"]
collection = db["aapl"]

client = RESTClient(config.API_KEY)

try:
    # Fetching Aggregates Data from Polygon.io
    aggs = client.get_aggs(
        "AAPL",
        1,
        "day",
        "2024-01-20",
        "2024-11-18"
    )

# Ensure `aggs` contains data
    if isinstance(aggs, list) and len(aggs) > 0:
        # Transform and insert into MongoDB
        documents = [
            {
                "open": agg.open,
                "high": agg.high,
                "low": agg.low,
                "close": agg.close,
                "volume": agg.volume,
                "vwap": agg.vwap,
                "timestamp": datetime.fromtimestamp(agg.timestamp / 1000),  # Convert to readable format
                "transactions": agg.transactions,
            }
            for agg in aggs
        ]
        collection.insert_many(documents)
        print("Data successfully inserted into MongoDB!")
    else:
        print("No data available to insert.")
except Exception as e:
    print("An error occurred:", e)
