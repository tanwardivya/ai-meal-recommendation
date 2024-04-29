import logging
import os
from typing import Any, Coroutine

import certifi
from loguru import logger
from motor.core import AgnosticCollection
import motor.motor_asyncio
from openai.types.beta import assistant

class DatabaseStore:
    db_client = None
    user_collection = None
    chat_collection = None
    @staticmethod
    async def startup():
        DatabaseStore.db_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_CONNECTION_STRING"), tlsCAFile=certifi.where())
        agent = DatabaseStore.db_client.agent
        DatabaseStore.user_collection = agent.get_collection("users")
        DatabaseStore.chat_collection = agent.get_collection("chats")
        logger.info('Database startup completed')
    
    @staticmethod
    async def shutdown():
        if DatabaseStore.db_client:
            DatabaseStore.db_client.close()
            logger.info('Database shutdown completed')
    
    @staticmethod
    def get_user_collection() -> AgnosticCollection:
        assert DatabaseStore.user_collection is not None
        return DatabaseStore.user_collection

    @staticmethod
    def get_chat_collection() -> AgnosticCollection:
        assert DatabaseStore.chat_collection is not None
        return DatabaseStore.chat_collection

    @staticmethod
    async def find_user(email:str, user_collection: AgnosticCollection):
        assert DatabaseStore.user_collection is not None
        existing_user = await user_collection.find_one(
            {"email": email}
        )
        return existing_user
    
    @staticmethod 
    async def find_chat( assistant_id: str, chat_collection: AgnosticCollection):
        assert DatabaseStore.chat_collection is not None
        existing_chat = await chat_collection.find_one(
            {"assistant_id": assistant_id}
        )
        return existing_chat
