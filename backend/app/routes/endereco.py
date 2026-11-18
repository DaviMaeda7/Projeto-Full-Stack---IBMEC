from fastapi import Depends, FastAPI, APIRouter
import pandas as pd
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Endereco
from app.schemas import EnderecoIn, EnderecoUpdateIn
from sqlalchemy import select, text

router = APIRouter(prefix="/enderecos")

@router.get("/pegar-mensagem")
def primeira_api():
    return {"message": "Hello World"}


@router.get("/pegar-dados-endereco")
def pegar_dados_endereco(db: Session = Depends(get_db)):
    enderecos = db.scalars(select(Endereco).order_by(Endereco.id)).all()
    return enderecos

@router.get("/pegar-dados-endereco-por-id/{id}")
def pegar_dados_endereco_por_id(id: int, db: Session = Depends(get_db)):
    endereco = db.get(Endereco, id)
    return endereco

@router.post("/criar-endereco")
def criar_endereco(endereco: EnderecoIn, db: Session = Depends(get_db)):
    dados = Endereco(
        cep = endereco.cep,
        endereco = endereco.endereco,
        bairro = endereco.bairro,
        cidade = endereco.cidade,
        estado = endereco.estado,
        regiao = endereco.regiao
    )
    db.add(dados)
    db.commit()

@router.delete("/deletar-endereco/{id}")
def deletar_endereco(id: int, db: Session = Depends(get_db)):
    dados = db.get(Endereco,  id)
    db.delete(dados)
    db.commit()
    return {"mensagem": "Endereço deletado com sucesso!"}

@router.put("/atualizar-endereco/{id}")
def atualizar_endereco(id: int, endereco: EnderecoUpdateIn, db: Session = Depends(get_db)):
    dados = db.get(Endereco, id)
    campos = endereco.model_dump(exclude_unset=True)
    for chave, valor in campos.items():
        setattr(dados, chave, valor)
    db.commit()
    return {"mensagem": "Endereço atualizado com sucesso!"}
