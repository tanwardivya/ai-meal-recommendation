import os

from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from loguru import logger
from passlib.context import CryptContext

from recipe_assistant.models.chat import ChatMetadata
from recipe_assistant.models.db.users import UserModel, ChatModel
from recipe_assistant.models.users import (
    LoginHttpRequest,
    LoginHttpResponse,
    RegisterHttpResponse,
    UserProfile,
)
from recipe_assistant.token_service import issue_token
from recipe_assistant.utils.assistant import create_assistant, create_thread
from recipe_assistant.utils.cache import InMemoryCache
from recipe_assistant.utils.db import DatabaseStore
from recipe_assistant.utils.openai_client import OpenAIClient

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/users/register", tags=["users"], response_model=RegisterHttpResponse)
async def register_user(request: Request):
    form_data = await request.form()
    hash_password = get_password_hash(str(form_data.get('password')))
    user_model = UserModel(
        firstname=str(form_data.get("firstname")),
        lastname=str(form_data.get("lastname")),
        email=str(form_data.get("email")),
        dietary_preference=str(form_data.get("dietary_preference")),
        location=str(form_data.get("location")),
        password=hash_password
    )
    user_collection = DatabaseStore.get_user_collection()
    existing_user = await DatabaseStore.find_user(user_model.email, user_collection)
    if existing_user:
        raise HTTPException(detail=f'User with email:{user_model.email} already exists', status_code=status.HTTP_400_BAD_REQUEST)

    assistant = create_assistant(client=OpenAIClient.client, assistant_name='Recipe Assistant', model_name=str(os.environ.get('OPENAI_MODEL_NAME')))
    user_model.assistant_id = assistant.id
    new_user = await user_collection.insert_one(user_model.model_dump(by_alias=True, exclude=set(['id'])))
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    logger.info('User registration complete')
    return RegisterHttpResponse(message='successful registration', username='_'.join([user_model.firstname.lower(), user_model.lastname.lower()]), id = str(created_user['_id'])) #type:ignore

@router.post("/users/login", tags=["users"],response_model=LoginHttpResponse)
async def login_user(login_request: LoginHttpRequest):
    user_collection = DatabaseStore.get_user_collection()
    existing_user = await DatabaseStore.find_user(login_request.email, user_collection)

    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with email {login_request.email} not found")
    if not verify_password(plain_password=login_request.password, hashed_password=existing_user['password']):
        raise HTTPException(detail=f'invalid password', status_code=status.HTTP_400_BAD_REQUEST)
    assistant_id = existing_user['assistant_id']
    thread = create_thread(client=OpenAIClient.client)
    chat_collection = DatabaseStore.get_chat_collection()
    chat_model = ChatModel(assistant_id=assistant_id,thread_id=thread.id)
    new_chat = await chat_collection.insert_one(chat_model.model_dump(by_alias=True, exclude=set(['id'])))
    logger.info('Succesfully created chat in database')
    InMemoryCache.create(key=existing_user['email'], value = ChatMetadata(assistant_id=assistant_id, thread_id=thread.id))
    user_id = '_'.join([existing_user['firstname'].lower(),existing_user['lastname'].lower()])
    token = issue_token(user_id=user_id, email=login_request.email)
    login_response = LoginHttpResponse(
        user=UserProfile(
            username=user_id,
            firstname=existing_user['firstname'],
            lastname=existing_user['lastname'],
            email=login_request.email),
        token=token)
    logger.info('Login is successfull')
    return login_response