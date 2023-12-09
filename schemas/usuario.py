from pydantic import BaseModel

class Usuario(BaseModel):
    email:          str | None
    password_login: str | None