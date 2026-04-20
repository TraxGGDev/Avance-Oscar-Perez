from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Reservas de Salas",
    version="1.0.0"
)
#Crear un nuevo usuario
@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session=Depends(get_db)):
    
    nuevo_usuario = models.Usuario(
        nombre = usuario.nombre
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return(nuevo_usuario)
#creamos una nueva sala
@app.post("/salas/", response_model=schemas.SalaResponse)
def crear_sala(sala: schemas.SalaCreate, db: Session=Depends(get_db)):
    
    salas = db.query(models.Sala).filter(models.Sala.numero_de_sala == sala.numero_de_sala).first()
    
    if sala in salas:
        raise HTTPException(status_code=400, detail="Esta sala ya esat registrada")
    
    nueva_sala = models.Sala(
        numero_de_sala = sala.numero_de_sala,
        capacidad = sala.capacidad,
        ubicacion = sala.ubicacion
    )
    
    db.add(nueva_sala)
    db.commit()
    db.refresh(nueva_sala)
    return nueva_sala

#ver lista de salas
@app.get("/salas/", response_model=list[schemas.SalaResponse])
def obtener_salas(db:Session=Depends(get_db)):
    
    salas = db.query(models.Sala).all()
    
    return salas

#Reservar una sala

@app.post("/reservas/", response_model=schemas.ReservaResponse)
def reservar_sala(reserva: schemas.ReservaCreate, db: Session=Depends(get_db)):
    
    sala = db.query(models.Sala).filter(models.Sala.id == reserva.sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="La sala no existe")
    
    nueva_reserva = models.Reserva(
        usuario_id = reserva.usuario_id,
        sala_id = reserva.sala_id,
        fecha = reserva.fecha,
        hora_inicio = reserva.hora_inicio,
        hora_fin = reserva.hora_fin
    )
    
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva

@app.get("/reservas/", response_model=list[schemas.ReservaResponse])
def obtener_reservas(db: Session=Depends(get_db)):
    
    reservas = db.query(models.Reserva).all()
    
    return reservas

@app.delete("/reservas/{reserva_id}")
def cancelar_reserva(reserva_id: int, db:Session=Depends(get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    
    if not reserva:
        raise HTTPException(status_code=404, detail="La reserva no existe")
    
    db.delete(reserva)
    db.commit()
    return {"mensaje": "Reserva eliminada correctamente"}