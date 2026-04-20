from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship
from database import Base

class Sala(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, index=True)
    numero_de_sala = Column(Integer)
    capacidad = Column(Integer)
    ubicacion = Column(String(100))
    
    reservas = relationship("Reserva", back_populates="sala")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column (Integer, primary_key=True, index=True)    
    nombre = Column(String(100))
    
    reservas = relationship("Reserva", back_populates="usuario")
    
class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    sala_id = Column(Integer, ForeignKey("salas.id"))
    fecha = Column(DateTime)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    usuario = relationship("Usuario", back_populates="reservas")
    sala = relationship("Sala", back_populates="reservas")
    
