from pydantic import BaseModel


class SignUpSchema(BaseModel):
    name: str = "someonidk"
    email: str = "someone@something.com"
    password: str = "somethingidk"



class SignInSchema(BaseModel):
    email: str = "someone@somethong.com"
    password: str = "someonethongidk"