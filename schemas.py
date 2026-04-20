from pydantic import BaseModel
from datetime import datetime, time

class SalaCreate(BaseModel):
    numero_de_sala: int
    capacidad: int
    ubicacion: str
    
class SalaResponse(BaseModel):
    id: int
    numero_de_sala: int
    capacidad: int
    ubicacion: str
    
    class Config:
        from_attributes=True
        
class UsuarioCreate(BaseModel):
    nombre: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    
    class Config:
        from_attributes=True

class ReservaCreate(BaseModel):
    usuario_id: int
    sala_id: int
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    
class ReservaResponse(BaseModel):
    id: int
    usuario: UsuarioResponse
    sala: SalaResponse
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    
    class Config:
        from_attributes=True
    
    