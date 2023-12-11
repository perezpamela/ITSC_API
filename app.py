import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel, inspect
from db.config import engine
from fastapi.middleware.cors import CORSMiddleware
from routes.sedes import sedes
from routes.alumnos import alumnos
from routes.carreras import carreras
from routes.sedecarrera import sedecarrera
from routes.inscripciones import inscripciones
from routes.pagos import pagos
from routes.docentes import docentes
from routes.preceptores import preceptores
from routes.materias import materias
from routes.materiacarrera import materiacarrera
from routes.horarios import horarios
from routes.clases import clases
from routes.examenes import examenes
from routes.cursantes import cursantes
from routes.asistencias import asistencias
from routes.notas import notas
from routes.login import login
from routes.auth import Verifica

from schemas.usuario import Usuario
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


APP = FastAPI(title='Instituto Técnico Superior Córdoba API', 
              description='API Gestión de datos ITSC | Prácticas Profesionalizantes II - Tec. Sup. en Desarrollo de Software')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@APP.post("/token")
def Generador_Token(form_data: OAuth2PasswordRequestForm = Depends()):
    usr = Usuario()
    usr.email = form_data.username
    usr.password_login = form_data.password
    verifica = Verifica(usr)
    if verifica == False or verifica == 404:
        raise HTTPException(status_code=401, detail='Los datos de acceso no son válidos.')
    else: 
        {"access_token": "token", "token_type": "bearer"}

@APP.get("/Endpoint_Privado/")
def Ejemplo_Ruta_Privada(token: str = Depends(oauth2_scheme)):
    return 'Funciona!! :)'


@APP.get('/')
def Inicio():
    return 'Hello World.'
APP.include_router(sedes)
APP.include_router(carreras)
APP.include_router(sedecarrera)
APP.include_router(alumnos)
APP.include_router(inscripciones)
APP.include_router(pagos)
APP.include_router(docentes)
APP.include_router(preceptores)
APP.include_router(materias)
APP.include_router(materiacarrera)
APP.include_router(horarios)
APP.include_router(clases)
APP.include_router(examenes)
APP.include_router(cursantes)
APP.include_router(asistencias)
APP.include_router(notas)
APP.include_router(login)

if __name__=='__main__':
    uvicorn.run('app:APP', reload=True)

@APP.on_event('startup')
def On_StartUp():
    SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    #tablas = inspector.get_table_names()
    #sedes_cols = inspector.get_columns("sedes")
    #print(sedes_cols)

# Configurar CORS
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

tags_metadata = [
    {"name": "Asistencias", "description": "Operaciones relacionadas con la tabla asistencias."},
    {"name": "Alumnos", "description": "Operaciones relacionadas con la tabla alumnos."},
    {"name": "Carreras", "description": "Operaciones relacionadas con la tabla carreras."},
    {"name": "Clases", "description": "Operaciones relacionadas con la tabla clases."},
    {"name": "Cursantes", "description": "Operaciones relacionadas con la tabla cursantes."},
    {"name": "Docentes", "description": "Operaciones relacionadas con la tabla docentes."},
    {"name": "Exámenes", "description": "Operaciones relacionadas con la tabla examenes."},
    {"name": "Horarios", "description": "Operaciones relacionadas con la tabla horarios."},
    {"name": "Inscripciones", "description": "Operaciones relacionadas con la tabla inscripciones."},
    {"name": "MateriaCarrera", "description": "Operaciones relacionadas con la tabla materiacarrera."},
    {"name": "Materias", "description": "Operaciones relacionadas con la tabla materias."},
    {"name": "Pagos", "description": "Operaciones relacionadas con la tabla pagos."},
    {"name": "Preceptores", "description": "Operaciones relacionadas con la tabla preceptores."},
    {"name": "SedeCarrera", "description": "Operaciones relacionadas con la tabla sedecarrera."},
    {"name": "Sedes", "description": "Operaciones relacionadas con la tabla sedes."},
    {"name": "Notas", "description": "Operaciones relacionadas con la tabla notas."},
    {"name": "Login", "description": "Verificación para loggeo."}
]
