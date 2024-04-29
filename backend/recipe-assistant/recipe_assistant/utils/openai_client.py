import os

from loguru import logger
from openai import OpenAI

class OpenAIClient:
    client : OpenAI

    @staticmethod
    def startup():
        OpenAIClient.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        logger.info('OpenAI client setup completed')

    @staticmethod
    def shutdown():
        if OpenAIClient.client:
            OpenAIClient.client.close()
            logger.info('OpenAI client shutdown completed')