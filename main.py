from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from jwtsign import sign, decode

app = FastAPI()

userlist = []

class SignUpSchema(BaseModel):
    name: str = "someonidk"
    email: str = "someone@something.com"
    password: str = "somethingidk"



@app.post("/signup")
def sign_up(request: SignUpSchema):
    # Проверка: уже зарегистрирован?
    for user in userlist:
        if user.email == request.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Если нет — добавляем
    userlist.append(request)

    # Генерим токен
    token = sign(request.email)

    return token



class SignInSchema(BaseModel):
    email: str = "someone@somethong.com"
    password: str = "someonethongidk"


@app.post("/signin")
def sign_in(request: SignInSchema):
    for user in userlist:
        if user.email == request.email:
            if user.password == request.password:
                token = sign(user.email)
                return token
            else:
                raise HTTPException(status_code=404, detail="Incorrect password")
    raise HTTPException(status_code=400, detail="Email not registered")

@app.post("/authtest")
def auth_test(decoded: str = Depends(decode)):
    return decoded