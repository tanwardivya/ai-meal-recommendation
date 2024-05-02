import os

from fastapi import APIRouter, HTTPException, Request, status, Response
from loguru import logger
from bson import ObjectId

from recipe_assistant.models.chat import (
    ChatMessage,
    ChatMetadata,
    ChatResponse,
    NewChatHttpRequest,
)
from recipe_assistant.token_service import decode_token
from recipe_assistant.utils.assistant import (
    create_run,
    get_response,
    wait_on_run,
    delete_thread,
    create_thread
)
from recipe_assistant.utils.cache import InMemoryCache
from recipe_assistant.utils.db import DatabaseStore
from recipe_assistant.models.db.users import ChatModel
from recipe_assistant.utils.openai_client import OpenAIClient

MODEL_NAME = os.environ.get('OPENAI_MODEL_NAME')

router = APIRouter()
IN_MEMORY_USER_MESSAGES = []

@router.post("/chat/new", tags=["chats"], response_model=ChatResponse)
async def new_chat(request: Request, new_chat_request: NewChatHttpRequest):
    if request.headers.get('Authorization') is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized access') 
    bearer_token = str(request.headers.get('Authorization'))
    token = bearer_token.split(' ')[1]
    payload = decode_token(token)
    chat_metadata = InMemoryCache.cache.get(payload['email'])
    if chat_metadata is None:
        thread_id = None
        logger.info('Fetching chat metadata from database')
        user_collection = DatabaseStore.get_user_collection()
        existing_user = await DatabaseStore.find_user(payload['email'], user_collection)
        if existing_user is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
        chat_collection = DatabaseStore.get_chat_collection()
        existing_chat = await DatabaseStore.find_chat(assistant_id=existing_user['assistant_id'], chat_collection=chat_collection)    
        if existing_chat  is None:
            thread = create_thread(client=OpenAIClient.client)
            thread_id = thread.id
            chat_model = ChatModel(assistant_id=existing_user['assistant_id'],thread_id=thread.id)
            new_chat = await chat_collection.insert_one(chat_model.model_dump(by_alias=True, exclude=set(['id'])))
            logger.info(f'Thread inserted in database:{thread_id}')
        else:
            thread_id = existing_chat['thread_id']
        InMemoryCache.create(key=existing_user['email'], value=ChatMetadata(assistant_id=existing_user['assistant_id'], thread_id=thread_id))
        chat_metadata = InMemoryCache.get(existing_user['email'])
    logger.info(f'chat_metadata:{chat_metadata}')
    thread_id = chat_metadata.thread_id
    assistant_id = chat_metadata.assistant_id
    run = create_run(client=OpenAIClient.client, assistant_id=assistant_id, thread_id=thread_id, user_input=new_chat_request.message)
    run = wait_on_run(client=OpenAIClient.client,thread_id=thread_id, run = run)
    response = get_response(client=OpenAIClient.client,thread_id=thread_id)
    chat_response = ChatMessage(role='assistant', content=response)
    chats = []
    chats.append(chat_response)
    logger.info('chat completion completed')
    return ChatResponse(chats=chats)
    

@router.delete("/chat/delete", tags=["chats"])
async def delete_chat(request: Request):
    if request.headers.get('Authorization') is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized access') 
    bearer_token = str(request.headers.get('Authorization'))
    token = bearer_token.split(' ')[1]
    payload = decode_token(token)
    user_collection = DatabaseStore.get_user_collection()
    existing_user = await DatabaseStore.find_user(payload['email'], user_collection)
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    chat_collection = DatabaseStore.get_chat_collection()
    existing_chat = await DatabaseStore.find_chat(assistant_id=existing_user['assistant_id'], chat_collection=chat_collection)
    if existing_chat  is None:
        InMemoryCache.cache.pop(key=payload['email'])
        logger.info('Removed from cache')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    delete_thread(client=OpenAIClient.client, thread_id=existing_chat['thread_id'])
    delete_result = await chat_collection.delete_one({"_id": ObjectId(str(existing_chat['_id']))})
    InMemoryCache.cache.pop(key=payload['email'])
    logger.info('Removed from cache')
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Chat not found")