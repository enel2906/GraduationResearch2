import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from pymongo import MongoClient

def draw_candlestick_chart():
    # MongoDB Connection
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["stock"]
    collection = db["aapl"]

    # Fetching data from MongoDB
    cursor = collection.find()
    data = list(cursor)

    # Check if the collection has data
    if not data:
        print("No data found in the MongoDB collection!")
        return

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Ensure necessary fields exist in the data
    required_fields = {"timestamp", "open", "high", "low", "close", "volume"}
    if not required_fields.issubset(df.columns):
        print(f"Missing required fields in data: {required_fields - set(df.columns)}")
        return

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Keep only necessary columns
    df = df[["open", "high", "low", "close", "volume"]]

    # Plot the candlestick chart
    mpf.plot(
        df,
        type="candle",
        volume=True,
        title="AAPL Candlestick Chart",
        style="yahoo"
    )

# Call the function
draw_candlestick_chart()
