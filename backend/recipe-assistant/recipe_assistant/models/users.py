from pydantic import BaseModel

class LoginHttpRequest(BaseModel):
    email: str
    password: str

class RegisterHttpRequest(LoginHttpRequest):
    first_name: str
    last_name: str
    dietary_preference: str
    location: str

class SuccessHttpResponse(BaseModel):
    message: str

class RegisterHttpResponse(SuccessHttpResponse):
    username: str
   

class ErrorHttpResponse(BaseModel):
    error_message: str

class UserProfile(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str

class LoginHttpResponse(BaseModel):
    user: UserProfile
    token: str





