from fastapi import APIRouter, HTTPException
from schemas.usuario import Usuario
import bcrypt
from routes.auth import Verifica

login = APIRouter(prefix='/API/LOGIN', tags=["Login"])


def Guarda_Password(p: str):
    hashed_p = bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode()
    return hashed_p


@login.post('/')
def Login(usuario: Usuario):
 password = Verifica(usuario)
 if password == True: 
    return True
 elif password == False:
    return False
 elif password == 404:
    return HTTPException(status_code=404, detail='El email ingresado no existe. ')
