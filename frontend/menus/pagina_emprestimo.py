from componentes.base_tela import TelaBase
import streamlit as st
from connection.base_api import BaseAPI
import pandas as pd

class EmprestimoTela(TelaBase):

  def __init__(self):
    self.base = BaseAPI()
    self.titulo = "Tela de Empréstimo"
    self.descricao = "Essa tela é usada para registrar e consultar empréstimos de livros"

  def consultar(self):
    endpoint = "/emprestimos/pegar-dados-emprestimos"
    dados = self.base.get(endpoint)
    return dados

  def consultar_por_id(self, id):
    endpoint = f"/emprestimos/pegar-dados-emprestimos-por-id/{id}"
    dados = self.base.get(endpoint)
    return dados

  def criar(self, params):
    endpoint = "/emprestimos/criar-emprestimo"
    return self.base.post(endpoint, params)

  def devolver(self, id):
    endpoint = f"/emprestimos/devolver-emprestimo/{id}"
    return self.base.put(endpoint)

  def criar_dataframe(self, dados):
    df = pd.DataFrame(dados)
    st.dataframe(df)

  def renderizar(self):
    super().cabecalho(self.titulo, self.descricao)
    abas = st.tabs(["Consultar todos", "Consultar por ID", "Registrar Empréstimo", "Registrar Devolução"])
    with abas[0]:
      dados = self.consultar()
      self.criar_dataframe(dados)
    with abas[1]:
      id = st.text_input("Digite o ID do empréstimo:")
      if st.button("Consultar empréstimo por ID"):
        dados = self.consultar_por_id(id)
        df = pd.DataFrame([dados])
        st.dataframe(df)
    with abas[2]:
      aluno_id = st.text_input("Digite o ID do aluno")
      livro_id = st.text_input("Digite o ID do livro")
      if st.button("Registrar empréstimo"):
        if not aluno_id or not livro_id:
          st.error("Digite o ID do aluno e o ID do livro")
        else:
          params = {
            "aluno_id": int(aluno_id),
            "livro_id": int(livro_id)
          }
          retorno = self.criar(params)
          if retorno.status_code == 200:
            st.success("Empréstimo registrado com sucesso")
          else:
            st.error(retorno.text)
    with abas[3]:
      id = st.text_input("Digite o ID do empréstimo que deseja devolver")
      if st.button("Registrar devolução"):
        if not id:
          st.error("Digite o ID do empréstimo")
        else:
          retorno = self.devolver(int(id))
          if retorno.status_code == 200:
            st.success("Devolução registrada com sucesso")
          else:
            st.error(retorno.text)
    super().rodape()

EmprestimoTela().renderizar()
