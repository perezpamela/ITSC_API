from fastapi import APIRouter, Depends, HTTPException, Response
from db.config import Session, Get_Session
from sqlmodel import select, and_
from models.notas import notas as t_notas
from models.cursantes import cursantes as t_cursantes
from models.alumnos import alumnos as t_alumnos
from models.examenes import examenes as t_examenes
from models.materiacarrera import materiacarrera as t_materiacarrera
from models.materias import materias as t_materias
from schemas.notas import Nota, NotaOUTPUT
from datetime import datetime
from starlette.status import HTTP_204_NO_CONTENT

notas = APIRouter(prefix='/API/NOTAS', tags=["Notas"])

@notas.get('/')
def Get_Notas(filtro_cursante: str = None, filtro_materia: str = None, session: Session = Depends(Get_Session)):
    resultado = []
    notas = session.execute(select(
        t_notas, t_cursantes, t_alumnos, t_examenes, t_materiacarrera, t_materias
    ).where(
        and_(
            t_notas.c.CURSANTE_ID == t_cursantes.c.CURSANTE_ID,
            t_cursantes.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
            t_notas.c.EXAMEN_ID == t_examenes.c.EXAMEN_ID,
            t_examenes.c.MATERIACARRERA_ID == t_materiacarrera.c.MATERIACARRERA_ID,
            t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID
        )
    )).fetchall()

    if filtro_cursante:
         notas = [nota for nota in notas if filtro_cursante.upper() in (nota.NOMBRE+' '+nota.APELLIDO).upper()]
    if filtro_materia:
        notas = [nota for nota in notas if  filtro_materia.upper() in nota.DESCRIPCION.upper()]

    for nota in notas:
        single = NotaOUTPUT()
        single.NOTA_ID= nota.NOTA_ID
        single.EXAMEN_ID= nota.EXAMEN_ID
        single.CURSANTE_ID=nota.CURSANTE_ID
        single.NOTA= nota.NOTA
        single.OBSERVACIONES= nota.OBSERVACIONES
        single.STATUS= nota.STATUS
        single.ADD_DATE= nota.ADD_DATE
        single.LAST_UPDATED_DATE= nota.LAST_UPDATED_DATE
        #Info relevante del alumno al que pertenece la nota.
        single.NOMBRE= nota.NOMBRE
        single.APELLIDO= nota.APELLIDO
        #Info relevante del examen al que pertenece la nota.
        single.FECHA_EXAMEN= nota.FECHA
        single.DESCRIPCION_EXAMEN= nota.DESCRIPCION
        single.ETAPA= nota.ETAPA
        single.TIPO= nota.TIPO
        single.MATERIACARRERA_ID= nota.MATERIACARRERA_ID
        single.DESCRIPCION_MATERIA= nota.DESCRIPCION_1
        single.CICLO_LECTIVO= nota.CICLO_LECTIVO
        single.CURSO= nota.CURSO
        resultado.append(single)
    
    return resultado

@notas.get('/{id}')
def Get_Nota(id: int, session: Session = Depends(Get_Session)):
    nota =  session.execute(select(
        t_notas, t_cursantes, t_alumnos, t_examenes, t_materiacarrera, t_materias
    ).where(
        and_(
            t_notas.c.NOTA_ID == id,
            t_notas.c.CURSANTE_ID == t_cursantes.c.CURSANTE_ID,
            t_cursantes.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
            t_notas.c.EXAMEN_ID == t_examenes.c.EXAMEN_ID,
            t_examenes.c.MATERIACARRERA_ID == t_materiacarrera.c.MATERIACARRERA_ID,
            t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID
        )
    )).first()
    
    if not nota:
        return HTTPException(status_code=404, detail='No se encontraron datos.')
    n = NotaOUTPUT()
    n.NOTA_ID= nota.NOTA_ID
    n.EXAMEN_ID= nota.EXAMEN_ID
    n.CURSANTE_ID= nota.CURSANTE_ID
    n.NOTA= nota.NOTA
    n.OBSERVACIONES= nota.OBSERVACIONES
    n.STATUS= nota.STATUS
    n.ADD_DATE= nota.ADD_DATE
    n.LAST_UPDATED_DATE= nota.LAST_UPDATED_DATE
        #Info relevante del alumno al que pertenece la nota.
    n.NOMBRE= nota.NOMBRE
    n.APELLIDO= nota.APELLIDO
        #Info relevante del examen al que pertenece la nota.
    n.FECHA_EXAMEN= nota.FECHA
    n.DESCRIPCION_EXAMEN= nota.DESCRIPCION
    n.ETAPA= nota.ETAPA
    n.TIPO= nota.TIPO
    n.MATERIACARRERA_ID= nota.MATERIACARRERA_ID
    n.DESCRIPCION_MATERIA= nota.DESCRIPCION_1
    n.CICLO_LECTIVO= nota.CICLO_LECTIVO
    n.CURSO= nota.CURSO

    return n

@notas.post('/add')
def Add_Nota(nota: Nota, session: Session = Depends(Get_Session)):
    new = {
    
    "EXAMEN_ID":    nota.EXAMEN_ID,
    "CURSANTE_ID":  nota.CURSANTE_ID,
    "NOTA":         nota.NOTA,
    "OBSERVACIONES":nota.OBSERVACIONES
    }
    resultado = session.execute(t_notas.insert().values(new))
    session.commit()
    id = resultado.inserted_primary_key[0]
    return session.execute(select(t_notas).where(t_notas.c.NOTA_ID == id)).first()

@notas.put('/update/{id}')
def Update_Nota(id: int, nota: Nota, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_notas).where(t_notas.c.NOTA_ID == id)).first()
    if old:
        new = {
    
    "EXAMEN_ID":    nota.EXAMEN_ID,
    "CURSANTE_ID":  nota.CURSANTE_ID,
    "NOTA":         nota.NOTA,
    "OBSERVACIONES":nota.OBSERVACIONES,
    "LAST_UPDATED_DATE": datetime.now()
    }
        session.execute(t_notas.update().values(new).where(t_notas.c.NOTA_ID == id))
        session.commit()
        return session.execute(select(t_notas).where(t_notas.c.NOTA_ID == id)).first()
    else:
        return HTTPException(status_code=404, detail='No se encontraron datos.')


@notas.delete('/delete/{id}')
def Delete_Nota(id: int, session: Session = Depends(Get_Session)):
    nota = session.execute(select(t_notas).where(t_notas.c.NOTA_ID == id)).first()
    if nota:
        session.execute(t_notas.delete().where(t_notas.c.NOTA_ID == id))
        session.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
    return HTTPException(status_code=404, detail="No se encontraron datos para el id seleccionado.")