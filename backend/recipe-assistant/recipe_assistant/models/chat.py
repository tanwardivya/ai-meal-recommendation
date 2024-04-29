from typing import List

from pydantic import BaseModel
class NewChatHttpRequest(BaseModel):
    message: str


class ChatMessage(BaseModel):
    role: str
    content: str

class ChatResponse(BaseModel):
    chats: List[ChatMessage]


class ChatMetadata(BaseModel):
    assistant_id: str
    thread_id: str
