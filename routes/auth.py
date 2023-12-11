from db.config import Session, engine
from schemas.usuario import Usuario
from models.alumnos import alumnos as t_alumnos
from models.docentes import docentes as t_docentes
from models.preceptores import preceptores as t_preceptores
from sqlmodel import select, union
import bcrypt


def Verifica(u: Usuario):
    with Session(engine) as session:
         q_alumnos = select(t_alumnos.c.PASSWORD).where(t_alumnos.c.EMAIL == u.email)
         q_docentes = select(t_docentes.c.PASSWORD).where(t_docentes.c.EMAIL == u.email)
         q_preceptores = select(t_preceptores.c.PASSWORD).where(t_preceptores.c.EMAIL == u.email)
         full_q = union(q_alumnos, q_preceptores, q_docentes)

         password = session.execute(full_q).first()

         if password: 
            return password[0].encode('utf-8') == bcrypt.hashpw(u.password_login.encode('utf-8'),password[0].encode('utf-8'))
         else: 
            return 404
         

