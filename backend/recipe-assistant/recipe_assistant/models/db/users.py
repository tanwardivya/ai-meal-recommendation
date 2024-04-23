from typing import List, Optional

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