import jwt
import os

SECRET = os.environ.get('JWT_SECRET')

def issue_token(user_id:str, email:str)->str:
    data = {
        "user_id" : user_id,
        "email": email
    }
    token = jwt.encode(
        payload = data,
        key = SECRET
    )
    return token
    
