import os

from fastapi import APIRouter, Request
from openai import OpenAI
from fastapi.responses import StreamingResponse

from recipe_assistant.models.chat import ChatMessage, NewChatHttpRequest, ChatResponse
from recipe_assistant.utils.assistant import stream_assistant_run, create_thread, wait_on_run, create_run, get_response
OPENAI_CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL_NAME = os.environ.get('OPENAI_MODEL_NAME')

router = APIRouter()
IN_MEMORY_USER_MESSAGES = []

@router.post("/chat/new", tags=["chats"], response_model=ChatResponse)
async def new_chat(request: Request, new_chat_request: NewChatHttpRequest):
    thread = create_thread(client=OPENAI_CLIENT)
    ASSISTANT_ID = 'asst_uF6EsS12fkci8jbBgigasgYL'
    run = create_run(client=OPENAI_CLIENT, assistant_id=ASSISTANT_ID, thread_id=thread.id,user_input=new_chat_request.message)
    run = wait_on_run(client=OPENAI_CLIENT,thread_id=thread.id, run = run)
    response = get_response(client=OPENAI_CLIENT,thread_id=thread.id)
    chat_response = ChatMessage(role='assistant', content=response)
    chats = []
    chats.append(chat_response)
    return ChatResponse(chats=chats)

