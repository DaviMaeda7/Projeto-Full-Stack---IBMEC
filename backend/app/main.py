
from fastapi import FastAPI
from app.routes import alunos, disciplinas, notas, endereco


app = FastAPI()

app.include_router(alunos.router)
app.include_router(endereco.router)
app.include_router(disciplinas.router)
app.include_router(notas.router)