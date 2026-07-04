from starlette import status
from typing import Annotated
from datetime import timedelta


import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

# needed schemas
from ..schemas.user_schema import CreateUserRequest, CreateUserResponse, TokenResponse

# needed models
from ..models import User

# needed services
from ..services.user_service import UserService

# needed dependencies
from ..dependencies import get_user_service, get_current_user, get_inference_gateway


def hash_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/")
async def get_user(CurrentUserDep: Annotated[User, Depends(get_current_user)]):
    return {"user": CurrentUserDep}


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(
    UserServiceDep: Annotated[UserService, Depends(get_user_service)],
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = await UserServiceDep.authenticate_user(form.username, form.password)
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossível validar usuário.")

    access_token = await UserServiceDep.create_access_token(user, timedelta(minutes=20))
    refresh_token = await UserServiceDep.create_refresh_token(user, timedelta(days=5))
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=5*24*60*60,
        path="/auth/refresh"
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def read_refresh_token(UserServiceDep: Annotated[UserService, Depends(get_user_service)], request: Request):

    new_access_token = UserServiceDep.refresh(request.cookies.get("refresh_token"))

    return new_access_token


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(UserServiceDep: Annotated[UserService, Depends(get_user_service)], payload: CreateUserRequest) -> CreateUserResponse:
    
    user_model = await UserServiceDep.create_user(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role
    )

    return CreateUserResponse(email=user_model.email, username=user_model.username, role=user_model.role)