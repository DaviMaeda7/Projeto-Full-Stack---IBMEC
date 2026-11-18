from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AlunoLivro, Livro
from app.schemas import LivroIn


def listar_livros(db: Session):
    return db.scalars(select(Livro).order_by(Livro.id)).all()


def buscar_livro(db: Session, livro_id: int) -> Livro:
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


def criar_livro(db: Session, dados: LivroIn) -> Livro:
    livro = Livro(titulo=dados.titulo.strip(), autor=dados.autor.strip())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


# Um livro esta emprestado quando existe um emprestimo dele ainda sem data de devolucao
def livro_esta_emprestado(db: Session, livro_id: int) -> bool:
    buscar_livro(db, livro_id)
    consulta = select(AlunoLivro.id).where(
        AlunoLivro.livro_id == livro_id,
        AlunoLivro.data_devolucao.is_(None),
    )
    return db.scalar(consulta) is not None
