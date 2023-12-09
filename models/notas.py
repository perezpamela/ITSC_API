from sqlmodel import Table, Column, ForeignKey, INTEGER, FLOAT, VARCHAR, DATE, DATETIME
from db.config import meta

notas = Table(
    'NOTAS',
    meta,
    Column('NOTA_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('EXAMEN_ID', INTEGER,  ForeignKey('EXAMENES.EXAMEN_ID', ondelete='SET NULL')),
    Column('CURSANTE_ID', INTEGER,  ForeignKey('CURSANTES.CURSANTE_ID', ondelete='SET NULL')),
    Column('NOTA', FLOAT),
    Column('OBSERVACIONES', VARCHAR(200)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)