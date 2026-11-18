from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EmprestimoIn, EmprestimoOut
from app.services import emprestimo_service

router = APIRouter(prefix="/emprestimos")


@router.get("/")
def primeira_api():
    return {"message": "rotas emprestimos"}


# Filtros opcionais: ?somente_ativos=true, ?aluno_id=1, ?livro_id=1
@router.get("/pegar-dados-emprestimos", response_model=list[EmprestimoOut])
def pegar_dados_emprestimos(
    somente_ativos: bool = False,
    aluno_id: Optional[int] = None,
    livro_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return emprestimo_service.listar_emprestimos(db, somente_ativos, aluno_id, livro_id)


@router.get("/pegar-dados-emprestimos-por-id/{id}", response_model=EmprestimoOut)
def pegar_dados_emprestimos_por_id(id: int, db: Session = Depends(get_db)):
    return emprestimo_service.buscar_emprestimo(db, id)


@router.post("/criar-emprestimo", response_model=EmprestimoOut)
def criar_emprestimo(emprestimo: EmprestimoIn, db: Session = Depends(get_db)):
    return emprestimo_service.criar_emprestimo(db, emprestimo)


# Registra a devolucao: preenche data_devolucao com a data de hoje
@router.put("/devolver-emprestimo/{id}", response_model=EmprestimoOut)
def devolver_emprestimo(id: int, db: Session = Depends(get_db)):
    return emprestimo_service.devolver_emprestimo(db, id)
