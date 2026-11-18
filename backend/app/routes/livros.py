from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LivroIn, LivroOut
from app.services import livro_service

router = APIRouter(prefix="/livros")


@router.get("/")
def primeira_api():
    return {"message": "rotas livros"}


@router.get("/pegar-dados-livros", response_model=list[LivroOut])
def pegar_dados_livros(db: Session = Depends(get_db)):
    return livro_service.listar_livros(db)


@router.get("/pegar-dados-livros-por-id/{id}", response_model=LivroOut)
def pegar_dados_livros_por_id(id: int, db: Session = Depends(get_db)):
    return livro_service.buscar_livro(db, id)


@router.post("/criar-livro", response_model=LivroOut)
def criar_livro(livro: LivroIn, db: Session = Depends(get_db)):
    return livro_service.criar_livro(db, livro)


# Informa se o livro esta emprestado agora (True) ou disponivel (False)
@router.get("/esta-emprestado/{id}")
def livro_esta_emprestado(id: int, db: Session = Depends(get_db)):
    return {"livro_id": id, "emprestado": livro_service.livro_esta_emprestado(db, id)}
