# Sistema de Reservas de Salas
**Equipo:** Oscar Pérez  
**Dominio:** Gestión de reservas de salas  
**Fecha:** Abril 2026

---

## ¿Qué problema resuelve?
El sistema permite gestionar la reserva de salas de manera organizada, evitando conflictos de disponibilidad. Los usuarios pueden registrarse, consultar las salas disponibles y realizar reservas especificando fecha y horario. Todo esto a través de una interfaz web sencilla conectada a una API REST.

---

## Estructura de la Base de Datos
| Tabla | Descripción | Relación |
|-------|-------------|----------|
| usuarios | Guarda el nombre de cada usuario del sistema | Se relaciona con reservas |
| salas | Guarda el número, capacidad y ubicación de cada sala | Se relaciona con reservas |
| reservas | Guarda cada reserva con fecha, hora inicio y hora fin | Pertenece a un usuario y a una sala |

---

## Rutas de la API
| Método | Ruta | Qué hace |
|--------|------|----------|
| POST | /usuarios/ | Crea un nuevo usuario |
| POST | /salas/ | Crea una nueva sala (verifica que no exista) |
| GET | /salas/ | Retorna la lista de todas las salas |
| POST | /reservas/ | Crea una reserva para un usuario y sala |
| GET | /reservas/ | Retorna la lista de todas las reservas |
| DELETE | /reservas/{id} | Elimina una reserva por su ID |

---

## ¿Cuál es la tarea pesada y por qué bloquea el sistema?
El endpoint `POST /reservas/` contiene un `time.sleep(5)` que simula el tiempo 
que tomaría verificar la disponibilidad de la sala en un sistema externo. Cuando 
un solo usuario hace una reserva, espera 5 segundos y recibe su respuesta. El 
problema ocurre cuando múltiples usuarios intentan reservar al mismo tiempo — 
como el servidor procesa las peticiones de forma síncrona, cada usuario debe 
esperar a que termine el anterior, por lo que el tiempo de espera se multiplica 
por el número de usuarios en cola.

---

## Cómo levantar el proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# 2. Crear las tablas en RDS
mysql -h db-actividades.cjlloajygmbn.us-east-1.rds.amazonaws.com -u admin -p < schema.sql

# 3. Crear el archivo .env con las variables de entorno
DB_HOST=db-actividades.cjlloajygmbn.us-east-1.rds.amazonaws.com
DB_USER=admin
DB_PASSWORD=tu_password
DB_NAME=db-actividades
DB_PORT=3306

# 4. Construir la imagen
docker build -t reservas-app .

# 5. Correr el contenedor
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  -p 8501:8501 \
  --name reservas-app \
  reservas-app

# 6. Abrir en el navegador
http://IP_EC2:8000/docs   ← Swagger / documentación de la API
http://IP_EC2:8501        ← Interfaz Streamlit
```

---

## Decisiones técnicas
Se eligió FastAPI como framework backend por su rendimiento y porque genera documentación automática en `/docs`, lo que facilita probar los endpoints sin herramientas externas. Para la base de datos se usó SQLAlchemy como ORM, lo que permite definir las tablas como clases Python y evitar escribir SQL manualmente. Las tablas se diseñaron separando usuarios, salas y reservas para mantener la información normalizada y evitar duplicidad de datos. El manejo de errores se implementó verificando la existencia de registros antes de cada operación, retornando códigos HTTP descriptivos como 404 cuando una sala no existe o 400 cuando se intenta registrar una sala duplicada. Lo más difícil de implementar fue la configuración de red en AWS, específicamente lograr que el contenedor en EC2 se conectara correctamente a Aurora RDS a través de la VPC.