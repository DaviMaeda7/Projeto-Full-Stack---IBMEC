from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Aluno, AlunoLivro
from app.schemas import EmprestimoIn
from app.services import livro_service


def listar_emprestimos(
    db: Session,
    somente_ativos: bool = False,
    aluno_id: Optional[int] = None,
    livro_id: Optional[int] = None,
):
    consulta = select(AlunoLivro).order_by(AlunoLivro.id)
    if somente_ativos:
        consulta = consulta.where(AlunoLivro.data_devolucao.is_(None))
    if aluno_id is not None:
        consulta = consulta.where(AlunoLivro.aluno_id == aluno_id)
    if livro_id is not None:
        consulta = consulta.where(AlunoLivro.livro_id == livro_id)
    return db.scalars(consulta).all()


def buscar_emprestimo(db: Session, emprestimo_id: int) -> AlunoLivro:
    emprestimo = db.get(AlunoLivro, emprestimo_id)
    if emprestimo is None:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return emprestimo


def criar_emprestimo(db: Session, dados: EmprestimoIn) -> AlunoLivro:
    if db.get(Aluno, dados.aluno_id) is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    livro_service.buscar_livro(db, dados.livro_id)

    # Regra: nao da para emprestar um livro que ainda nao foi devolvido
    if livro_service.livro_esta_emprestado(db, dados.livro_id):
        raise HTTPException(status_code=409, detail="Livro já está emprestado")

    emprestimo = AlunoLivro(
        aluno_id=dados.aluno_id,
        livro_id=dados.livro_id,
        data_emprestimo=date.today(),
    )
    db.add(emprestimo)
    try:
        db.commit()
    except IntegrityError:
        # Dois pedidos ao mesmo tempo: o indice unico do banco barrou o segundo
        db.rollback()
        raise HTTPException(status_code=409, detail="Livro já está emprestado")
    db.refresh(emprestimo)
    return emprestimo


def devolver_emprestimo(db: Session, emprestimo_id: int) -> AlunoLivro:
    emprestimo = buscar_emprestimo(db, emprestimo_id)
    if emprestimo.data_devolucao is not None:
        raise HTTPException(status_code=409, detail="Livro já foi devolvido")
    emprestimo.data_devolucao = date.today()
    db.commit()
    db.refresh(emprestimo)
    return emprestimo
