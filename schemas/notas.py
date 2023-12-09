from pydantic import BaseModel
from datetime import date, datetime

class Nota(BaseModel):
    NOTA_ID:           int | None
    EXAMEN_ID:         int | None
    CURSANTE_ID:       int | None
    NOTA:              float | None
    OBSERVACIONES:     str | None
    STATUS:            int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None

class NotaOUTPUT(Nota):
    #Info relevante del alumno al que pertenece la nota.
    NOMBRE:              str| None
    APELLIDO:            str | None
    #Info relevante del examen al que pertenece la nota.
    FECHA_EXAMEN:        date | None
    DESCRIPCION_EXAMEN:  str | None
    ETAPA:               int | None
    TIPO:                str | None 
    MATERIACARRERA_ID:   int | None
    DESCRIPCION_MATERIA: str | None
    CICLO_LECTIVO:       str | None
    CURSO:               int | None