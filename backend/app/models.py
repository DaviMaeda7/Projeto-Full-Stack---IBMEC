from typing import Optional
from datetime import date
from sqlalchemy import Index, String, text, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy import String, Float, ForeignKey

class Aluno(Base):
    __tablename__ = 'tb_alunos'
    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(20))
    nome_aluno: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    endereco_id: Mapped[int] = mapped_column(ForeignKey('tb_enderecos.id'))

class Endereco(Base):
    __tablename__ = 'tb_enderecos'
    id: Mapped[int] = mapped_column(primary_key=True)
    cep: Mapped[str] = mapped_column(String(10), unique=True)
    endereco: Mapped[str] = mapped_column(String(255))
    bairro: Mapped[str] = mapped_column(String(255))
    cidade: Mapped[str] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(2))
    regiao: Mapped[str] = mapped_column(String(255))


class Disciplina(Base):
    __tablename__ = 'tb_disciplinas'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome_disciplina: Mapped[str] = mapped_column(String(255))
    carga: Mapped[str] = mapped_column(String(255))
    semestre: Mapped[str] = mapped_column(String(255))


class Nota(Base):
    __tablename__ = 'tb_notas'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome_id: Mapped[int] = mapped_column(ForeignKey('tb_alunos.id'))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey('tb_disciplinas.id'))
    nota: Mapped[float] = mapped_column(Float)

class Livro(Base):
    __tablename__ = 'tb_livros'
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    autor: Mapped[str] = mapped_column(String(255))


# Tabela associativa ALUNO_LIVRO: cada linha e um emprestimo de um livro para um aluno.
# data_devolucao vazia (NULL) = o livro ainda esta emprestado.
class AlunoLivro(Base):
    __tablename__ = 'tb_aluno_livro'
    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey('tb_alunos.id'))
    livro_id: Mapped[int] = mapped_column(ForeignKey('tb_livros.id'))
    data_emprestimo: Mapped[date] = mapped_column(Date, default=date.today)
    data_devolucao: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Um livro so pode ter UM emprestimo em aberto por vez (garantido pelo proprio banco)
    __table_args__ = (
        Index(
            'uq_livro_emprestimo_aberto',
            'livro_id',
            unique=True,
            postgresql_where=text('data_devolucao IS NULL'),
        ),
    )