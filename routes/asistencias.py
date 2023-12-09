from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_204_NO_CONTENT
from sqlmodel import select, and_, or_
from db.config import Session, Get_Session
from models.asistencias import asistencias as t_asistencias
from models.cursantes import cursantes as t_cursantes
from models.alumnos import alumnos as t_alumnos
from models.materiacarrera import materiacarrera as t_materiacarrera
from models.materias import materias as t_materias
from schemas.asistencias import AsistenciaOUTPUT
from models.clases import clases as t_clases
from schemas.asistencias import Asistencia
from datetime import datetime



asistencias = APIRouter(prefix='/API/ASISTENCIAS', tags=["Asistencias"])

@asistencias.get('/')#, summary='Devuelve toda la info de las asistencias cargadas en la tabla.')
def Get_Asistencias(filtro_alumno: str = None, filtro_materia: str = None, filtro_tema: str = None, session: Session = Depends(Get_Session)):
    '''
    Devuelve la información de las asistencias, incluyendo información relevante de tablas relacionadas.
    Opcionalmente, puede filtrar por: nombre/apellido alumno, descripcion materia o descripción de la clase (tema).
    '''
    result = []

    
    asistencias = session.execute(select(t_asistencias,
                                         t_cursantes, 
                                         t_alumnos, 
                                         t_clases,
                                         t_materiacarrera, 
                                         t_materias).where(
                                                and_(
                                                    t_asistencias.c.CURSANTE_ID == t_cursantes.c.CURSANTE_ID,
                                                    t_cursantes.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                                                    t_asistencias.c.CLASE_ID == t_clases.c.CLASE_ID,
                                                    t_clases.c.MATERIACARRERA_ID == t_materiacarrera.c.MATERIACARRERA_ID,
                                                    t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID
                                                    ))).fetchall()
 
    if filtro_alumno: 
        asistencias = [asistencia for asistencia in asistencias if filtro_alumno.upper() in (asistencia.NOMBRE+' '+asistencia.APELLIDO).upper()]
    if filtro_materia:
        asistencias = [asistencia for asistencia in asistencias if filtro_materia.upper() in asistencia.DESCRIPCION_1.upper()]
    if filtro_tema:
        asistencias = [asistencia for asistencia in asistencias if filtro_tema.upper() in asistencia.DESCRIPCION.upper()]

    for a in asistencias:
        single = AsistenciaOUTPUT()
        single.ASISTENCIA_ID = a.ASISTENCIA_ID
        single.CLASE_ID = a.CLASE_ID
        single.CURSANTE_ID = a.CURSANTE_ID
        single.ASISTENCIA = a.ASISTENCIA
        single.JUSTIFICADO = a.JUSTIFICADO
        single.OBSERVACIONES = a.OBSERVACIONES
        single.NOMBRE = a.NOMBRE
        single.APELLIDO = a.APELLIDO
        single.DESCRIPCION_MATERIA = a.DESCRIPCION_1
        single.DESCRIPCION_CLASE = a.DESCRIPCION
        single.ADD_DATE = a.ADD_DATE
        single.STATUS = a.STATUS
        single.LAST_UPDATED_DATE = a.LAST_UPDATED_DATE
        result.append(single)

    return result

@asistencias.get('/{id}')
def Get_Asistencia(id:int, session: Session = Depends(Get_Session)):
    '''
    Busca una asistencia filtrando por el id.
    '''
    asistencia = session.execute(select(t_asistencias,
                                         t_cursantes, 
                                         t_alumnos, 
                                         t_clases,
                                         t_materiacarrera, 
                                         t_materias).where(
                                                and_(
                                                    t_asistencias.c.ASISTENCIA_ID == id,
                                                    t_asistencias.c.CURSANTE_ID == t_cursantes.c.CURSANTE_ID,
                                                    t_cursantes.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                                                    t_asistencias.c.CLASE_ID == t_clases.c.CLASE_ID,
                                                    t_clases.c.MATERIACARRERA_ID == t_materiacarrera.c.MATERIACARRERA_ID,
                                                    t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID
                                                    ))).first()
    if not asistencia:
        return HTTPException(status_code=404,detail='La asistencia solicitada no existe.')
    
    result = AsistenciaOUTPUT()
    result.ASISTENCIA_ID = asistencia.ASISTENCIA_ID
    result.CLASE_ID = asistencia.CLASE_ID
    result.CURSANTE_ID = asistencia.CURSANTE_ID
    result.ASISTENCIA = asistencia.ASISTENCIA
    result.JUSTIFICADO = asistencia.JUSTIFICADO
    result.OBSERVACIONES = asistencia.OBSERVACIONES
    result.NOMBRE = asistencia.NOMBRE
    result.APELLIDO = asistencia.APELLIDO
    result.DESCRIPCION_MATERIA = asistencia.DESCRIPCION_1
    result.DESCRIPCION_CLASE = asistencia.DESCRIPCION
    result.ADD_DATE = asistencia.ADD_DATE
    result.STATUS = asistencia.STATUS
    result.LAST_UPDATED_DATE = asistencia.LAST_UPDATED_DATE

    return result

@asistencias.post('/add')
def Add_Asistencia(asistencia: Asistencia, session: Session = Depends(Get_Session)):
    ''' 
    Recibe un obj de tipo Asistencia y lo inserta en la tabla.
    '''
 
    new = {
    "CLASE_ID":       asistencia.CLASE_ID,
    "CURSANTE_ID":    asistencia.CURSANTE_ID, 
    "ASISTENCIA":     asistencia.ASISTENCIA,
    "JUSTIFICADO":    asistencia.JUSTIFICADO,
    "OBSERVACIONES":  asistencia.OBSERVACIONES
    }

    resultado = session.execute(t_asistencias.insert().values(new))
    session.commit()

    id = resultado.inserted_primary_key[0]
    asistencia = session.execute(select(t_asistencias).where(t_asistencias.c.ASISTENCIA_ID == id)).first()

    return asistencia


@asistencias.put('/update/{id}')
def Update_Asistencia(id: int, asistencia: Asistencia, session: Session = Depends(Get_Session)):
    '''
    Recibe un obj Asistencia y un id correspondiente a un registro de la tabla asistencias. \n 
    **Este update PISA los valores existentes, enviar todos los campos aunque se modifiquen solo algunos.
    '''
    
    old = session.execute(select(t_asistencias).where(t_asistencias.c.ASISTENCIA_ID == id)).first()
    if old:
        new = {
            "CLASE_ID":       asistencia.CLASE_ID,
            "CURSANTE_ID":    asistencia.CURSANTE_ID, 
            "ASISTENCIA":     asistencia.ASISTENCIA,
            "JUSTIFICADO":    asistencia.JUSTIFICADO,
            "OBSERVACIONES":  asistencia.OBSERVACIONES,
            "LAST_UPDATED_DATE": datetime.now()
        }

        session.execute(t_asistencias.update().values(new).where(t_asistencias.c.ASISTENCIA_ID == id))
        session.commit()
        return session.execute(select(t_asistencias).where(t_asistencias.c.ASISTENCIA_ID == id)).first()

    else:
        return HTTPException(status_code=404, detail='No se encontraron asistencias con el ID indicado.')

@asistencias.delete('/delete/{id}')
def Delete_Asistencia(id: int, session: Session = Depends(Get_Session)):
    '''
    Recibe un id de la tabla asistencias y lo borra.
    '''
    asistencia = session.execute(select(t_asistencias).where(t_asistencias.c.ASISTENCIA_ID == id)).first()

    if asistencia: 
        session.execute(t_asistencias.delete().where(t_asistencias.c.ASISTENCIA_ID == id))
        session.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
    return HTTPException(status_code=404,detail='El id indicado no existe.')
