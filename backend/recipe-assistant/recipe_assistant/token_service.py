from typing import Any, Dict
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
    

def decode_token(token: str) -> Dict[str, Any]:

    payload = jwt.decode(jwt=token, key= SECRET, algorithms=["HS256"])
    return payload