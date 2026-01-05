from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "deepfake_db")

client = None
db = None

def connect_db():
    global client, db
    try:
        client = MongoClient(MONGODB_URL)
        db = client[DB_NAME]
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")

def get_db():
    if db is None:
        connect_db()
    return db

def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")
