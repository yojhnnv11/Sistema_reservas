from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.routers import usuarios, canchas, reservas
from app.models import models as models_module  # Importa todos los modelos

# Crear automáticamente las tablas en PostgreSQL
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Sistema Reservas API (PostgreSQL)")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(canchas.router)
app.include_router(reservas.router)

@app.get("/")
def root():
    return {"msg": "API funcionando correctamente en Render"}
