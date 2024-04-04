from fastapi import APIRouter, Request
from recipe_assistant.models.users import LoginHttpResponse, RegisterHttpRequest,LoginHttpRequest, RegisterHttpResponse, UserProfile
router = APIRouter()

@router.post("/users/register", tags=["users"], response_model=RegisterHttpResponse)
async def register_user(request: Request):
    form_data = await request.form()
    return RegisterHttpResponse(message='successful registration', username='john_doe')

@router.post("/users/login", tags=["users"],response_model=LoginHttpResponse)
async def login_user(login_request: LoginHttpRequest):
    login_response = LoginHttpResponse(
        user=UserProfile(
            username="john_doe",
            firstname="John",
            lastname="Doe",
            email="johndoe@email.com"),
        token="user-fake-token")
    return login_response

@router.get("/users/profile/{username}", tags=["users"])
async def user_profile(username: str):
    return {"username": username}