from pydantic import BaseModel
from datetime import datetime, date

class Asistencia(BaseModel):
    ASISTENCIA_ID:     int | None
    CLASE_ID:          int | None
    CURSANTE_ID:       int | None
    ASISTENCIA:        int | None
    JUSTIFICADO:       int | None
    OBSERVACIONES:     str | None
    STATUS:            int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None


class AsistenciaOUTPUT(Asistencia):
    NOMBRE:              str | None
    APELLIDO:            str | None
    DESCRIPCION_MATERIA: str | None
    DESCRIPCION_CLASE:   str | None


    
