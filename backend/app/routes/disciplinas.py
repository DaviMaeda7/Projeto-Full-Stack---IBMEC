from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.orm import Session
from app.models import Disciplina
from app.schemas import DisciplinaIn, DisciplinaUpdateIn
import pandas as pd
from app.database import engine, get_db
from sqlalchemy import select, text

router = APIRouter(prefix="/disciplinas")

@router.get("/pegar-mensagem")
def primeira_api():
    return {"message": "disciplinas"}

@router.get("/pegar-dados-disciplina")
def pegar_dados_disciplina(db: Session = Depends(get_db)):
    disciplinas = db.scalars(select(Disciplina).order_by(Disciplina.id)).all()
    return disciplinas

@router.post("/criar-disciplina")
def criar_disciplina(disciplina: DisciplinaIn, db: Session = Depends(get_db)):
    dados = Disciplina(
        nome_disciplina = disciplina.nome_disciplina,
        carga = disciplina.carga,
        semestre = disciplina.semestre
    )
    db.add(dados)
    db.commit()

@router.put("/atualizar-disciplina/{id}")
def atualizar_disciplina(id: int, disciplina: DisciplinaUpdateIn, db: Session = Depends(get_db)):
    dados = db.get(Disciplina,  id)
    campos = disciplina.model_dump(exclude_unset=True)
    for campo, valor in campos.items():
        setattr(dados, campo, valor)
    db.commit()
    return {"mensagem": "Disciplina atualizada com sucesso!"}

@router.delete("/deletar-disciplina/{id}")
def deletar_disciplina(id: int, db: Session = Depends(get_db)):
    dados = db.get(Disciplina,  id)
    db.delete(dados)
    db.commit()
    return {"mensagem": "Disciplina deletada com sucesso!"}