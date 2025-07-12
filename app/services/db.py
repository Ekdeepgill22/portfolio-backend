# MongoDB operations
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None # type: ignore
    database: AsyncIOMotorDatabase = None # type: ignore


mongodb = MongoDB()


async def connect_to_mongo():
    """Create database connection"""
    logger.info(f"Connecting to MongoDB at URI: {settings.mongodb_uri}, DB: {settings.database_name}")
    try:
        # Add connection options for better resilience
        mongodb.client = AsyncIOMotorClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=30000,  # 30 seconds
            connectTimeoutMS=20000,  # 20 seconds
            socketTimeoutMS=20000,  # 20 seconds
            maxPoolSize=10,
            minPoolSize=1,
            retryWrites=True,
            retryReads=True
        )
        mongodb.database = mongodb.client[settings.database_name]
        
        # Test the connection
        await mongodb.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Create indexes for better performance
        await create_indexes()
        
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        raise e


async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        logger.info("MongoDB connection closed")


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Create index on email and created_at for contacts collection
        contacts_collection = mongodb.database.contacts
        await contacts_collection.create_index("email")
        await contacts_collection.create_index("created_at")
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")


def get_database() -> AsyncIOMotorDatabase: # type: ignore
    """Get database instance"""
    return mongodb.database


# Database service functions
async def insert_contact(contact_data: dict) -> str:
    """Insert a new contact form submission"""
    try:
        contacts_collection = mongodb.database.contacts
        result = await contacts_collection.insert_one(contact_data)
        logger.info(f"Contact form submission inserted with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error inserting contact: {e}")
        raise e


async def get_contact_by_id(contact_id: str) -> dict:
    """Get a contact by ID"""
    try:
        from bson import ObjectId
        contacts_collection = mongodb.database.contacts
        contact = await contacts_collection.find_one({"_id": ObjectId(contact_id)})
        return contact
    except Exception as e:
        logger.error(f"Error getting contact by ID: {e}")
        raise e


async def get_all_contacts(skip: int = 0, limit: int = 50) -> list:
    """Get all contacts with pagination"""
    try:
        contacts_collection = mongodb.database.contacts
        cursor = contacts_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        contacts = await cursor.to_list(length=limit)
        return contacts
    except Exception as e:
        logger.error(f"Error getting contacts: {e}")
        raise e