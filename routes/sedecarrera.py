from fastapi import APIRouter, Depends
from db.config import Session, Get_Session
from sqlmodel import select
from schemas.sedecarrera import SCarrera, SCarreraOUTPUT
from models.sedecarrera import sedecarrera as t_scarrera
from models.sedes import sedes as t_sedes
from models.carreras import carreras as t_carreras

sedecarrera = APIRouter(prefix='/API/SEDECARRERA')

@sedecarrera.get('/{id}')
def Get_Sedecarrera(id: int,session: Session = Depends(Get_Session)):
    #En este caso, que trae datos de dos entidades, devolver un schema personalizado.
    scarrera = SCarreraOUTPUT()
    sc = session.execute(select(t_scarrera).where(t_scarrera.c.SEDECARRERA_ID == id)).first()
    s  = session.execute(select(t_sedes).where(t_sedes.c.SEDE_ID == sc.SEDE_ID)).first()
    c  = session.execute(select(t_carreras).where(t_carreras.c.CARRERA_ID == sc.CARRERA_ID)).first()
    
    if sc:
        scarrera.SEDECARRERA_ID = sc.SEDECARRERA_ID
        scarrera.TURNO = sc.TURNO
        scarrera.CODIGO_CARRERA = sc.CODIGO_CARRERA
        scarrera.STATUS = sc.STATUS
        scarrera.ADD_DATE = sc.ADD_DATE
        scarrera.LAST_UPDATED_DATE = sc.LAST_UPDATED_DATE
    if c:
        scarrera.TITULO_CARRERA = c.DESCRIPCION
        scarrera.PLAN_START_DATE = c.PLAN_START_DATE
        scarrera.PLAN_END_DATE = c.PLAN_END_DATE
    if s:
        scarrera.SEDE_DESCRIPCION = s.DESCRIPCION
        scarrera.SEDE_DIRECCION = s.DIRECCION
        scarrera.SEDE_BARRIO = s.BARRIO
        scarrera.SEDE_LOCALIDAD = s.LOCALIDAD
        scarrera.SEDE_HORARIO_DESDE = s.HORA_DESDE
        scarrera.SEDE_HORARIO_HASTA = s.HORA_HASTA
        scarrera.SEDE_DIA_DESDE = s.DIA_DESDE
        scarrera.SEDE_DIA_HASTA = s.DIA_HASTA

    return scarrera