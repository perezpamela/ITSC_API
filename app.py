import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel, inspect
from db.config import engine
from routes.sedes import sedes
from routes.alumnos import alumnos
from routes.carreras import carreras
from routes.sedecarrera import sedecarrera
from routes.inscripciones import inscripciones
from routes.pagos import pagos


APP = FastAPI(title='Instituto Técnico Superior Córdoba API', 
              description='API para proyecto final Prácticas Profesionalizantes II - Tec. Sup. en Desarrollo de Software')

@APP.get('/')
def Inicio():
    return 'Hello World.'
APP.include_router(sedes)
APP.include_router(carreras)
APP.include_router(sedecarrera)
APP.include_router(alumnos)
APP.include_router(inscripciones)
APP.include_router(pagos)

if __name__=='__main__':
    uvicorn.run('app:APP', reload=True)

@APP.on_event('startup')
def On_StartUp():
    SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    #tablas = inspector.get_table_names()
    #sedes_cols = inspector.get_columns("sedes")
    #print(sedes_cols)