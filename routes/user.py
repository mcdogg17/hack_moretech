from fastapi import APIRouter, Depends, HTTPException, Response
from controllers.controllers import UserController
from passlib.context import CryptContext
from schemas.schema import UserLogin

router = APIRouter(prefix="/user", tags=["user"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login/")
def login_user(user: UserLogin, users: UserController = Depends()):
    '''
    Функция для авторизации пользователя по логину и паролю
    '''
    user = users.get_user_by_login(username)

    if user is None:
        raise HTTPException(status_code=400, detail="Неправильное имя пользователя или пароль")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Неправильное имя пользователя или пароль")

    response = Response(status_code=200)
    return response
