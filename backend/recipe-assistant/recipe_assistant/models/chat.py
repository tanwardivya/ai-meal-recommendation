from pydantic import BaseModel
from typing import List
class NewChatHttpRequest(BaseModel):
    message: str


class ChatMessage(BaseModel):
    role: str
    content: str

class ChatResponse(BaseModel):
    chats: List[ChatMessage]