from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from config.auth import ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context
from models.user_model import User, User_Pydantic, UserIn_Pydantic

from utils.auth import authenticate_user, create_access_token, get_current_user

auth = APIRouter(prefix="/api/v1", tags=["auth"])


@auth.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Invalid username or password'
    )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=pwd_context.hash(user.password_hash), email=user.email, first_name=user.first_name, last_name=user.last_name)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@auth.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user