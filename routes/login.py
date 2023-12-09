from fastapi import APIRouter, Depends, HTTPException
from schemas.usuario import Usuario
from db.config import Session, Get_Session
from models.alumnos import alumnos as t_alumnos
from models.docentes import docentes as t_docentes
from models.preceptores import preceptores as t_preceptores
from sqlmodel import select, union
import bcrypt

login = APIRouter(prefix='/API/LOGIN', tags=["Login"])


def Guarda_Password(p: str):
    hashed_p = bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode()
    return hashed_p

@login.post('/')
def Login(usuario: Usuario = None, session: Session = Depends(Get_Session)):
 
 q_alumnos = select(t_alumnos.c.PASSWORD).where(t_alumnos.c.EMAIL == usuario.email)
 q_docentes = select(t_docentes.c.PASSWORD).where(t_docentes.c.EMAIL == usuario.email)
 q_preceptores = select(t_preceptores.c.PASSWORD).where(t_preceptores.c.EMAIL == usuario.email)
 full_q = union(q_alumnos, q_preceptores, q_docentes)

 password = session.execute(full_q).first()

 if password: 
    return password[0].encode('utf-8') == bcrypt.hashpw(usuario.password_login.encode('utf-8'),password[0].encode('utf-8'))
 else: 
   return HTTPException(status_code=404, detail='El mail no está registrado.')
