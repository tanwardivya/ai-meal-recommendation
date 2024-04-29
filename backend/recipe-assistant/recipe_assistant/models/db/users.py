from typing import Optional

from openai.types.beta import assistant
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]
class UserModel(BaseModel):
    """
    Container for a single user record.
    """
    # The primary key for the UserModel, stored as a `str` on the instance.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    firstname: str = Field(...)
    lastname: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    location: str = Field(...)
    dietary_preference: str = Field(...)
    assistant_id: str | None = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firstname": "Jane",
                "lastname": "Doe",
                "email": "jdoe@example.com",
                "location": "California",
                "dietary_preference":"Vegan, Gluten Free"
            }
        },
    )

class ChatModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    assistant_id: str = Field(...)
    thread_id: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "assistant_id": "asst_217w172wt",
                "thread_id": "thread_wiwi2682",
            }
        },
    )
