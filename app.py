import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel, inspect
from db.config import engine
from routes.sedes import sedes

APP = FastAPI(title='Instituto Técnico Superior Córdoba API')

@APP.get('/')
def Inicio():
    return 'Hello World.'
APP.include_router(sedes)

if __name__=='__main__':
    uvicorn.run('app:APP', reload=True)

@APP.on_event('startup')
def On_StartUp():
    SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    #tablas = inspector.get_table_names()
    #sedes_cols = inspector.get_columns("sedes")
    #print(sedes_cols)