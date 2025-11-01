"""Database connection and configuration."""
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/netsage_ml")

# Synchronous client for synchronous operations
_client = None
_db = None

# Asynchronous client for async operations
_async_client = None
_async_db = None


def get_client():
    """Get synchronous MongoDB client."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def get_database():
    """Get synchronous database instance."""
    global _db
    if _db is None:
        client = get_client()
        # Extract database name from URI or use default
        if "/" in MONGO_URI.split("mongodb://")[-1]:
            db_name = MONGO_URI.split("/")[-1].split("?")[0]
        else:
            db_name = "netsage_ml"
        _db = client[db_name]
    return _db


def get_async_client():
    """Get asynchronous MongoDB client."""
    global _async_client
    if _async_client is None:
        _async_client = AsyncIOMotorClient(MONGO_URI)
    return _async_client


def get_async_database():
    """Get asynchronous database instance."""
    global _async_db
    if _async_db is None:
        client = get_async_client()
        if "/" in MONGO_URI.split("mongodb://")[-1]:
            db_name = MONGO_URI.split("/")[-1].split("?")[0]
        else:
            db_name = "netsage_ml"
        _async_db = client[db_name]
    return _async_db

