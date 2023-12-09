from sqlmodel import Table, Column, ForeignKey, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

asistencias = Table(
    'ASISTENCIAS',
    meta,
    Column('ASISTENCIA_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('CLASE_ID', INTEGER, ForeignKey('CLASES.CLASE_ID', ondelete='SET NULL')),
    Column('CURSANTE_ID', INTEGER, ForeignKey('CURSANTES.CURSANTE_ID', ondelete='SET NULL')),
    Column('ASISTENCIA', INTEGER),
    Column('JUSTIFICADO', INTEGER),
    Column('OBSERVACIONES', NVARCHAR(200)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)