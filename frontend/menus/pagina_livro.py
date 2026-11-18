from componentes.base_tela import TelaBase
import streamlit as st
from connection.base_api import BaseAPI
import pandas as pd

class LivroTela(TelaBase):

  def __init__(self):
    self.base = BaseAPI()
    self.titulo = "Tela de Livro"
    self.descricao = "Essa tela é usada para cadastrar e consultar livros"

  def consultar(self):
    endpoint = "/livros/pegar-dados-livros"
    dados = self.base.get(endpoint)
    return dados

  def consultar_por_id(self, id):
    endpoint = f"/livros/pegar-dados-livros-por-id/{id}"
    dados = self.base.get(endpoint)
    return dados

  def criar(self, params):
    endpoint = "/livros/criar-livro"
    return self.base.post(endpoint, params)

  def esta_emprestado(self, id):
    endpoint = f"/livros/esta-emprestado/{id}"
    dados = self.base.get(endpoint)
    return dados

  def criar_dataframe(self, dados):
    df = pd.DataFrame(dados)
    st.dataframe(df)

  def renderizar(self):
    super().cabecalho(self.titulo, self.descricao)
    abas = st.tabs(["Consultar todos", "Consultar por ID", "Criar Livro", "Livro está emprestado?"])
    with abas[0]:
      dados = self.consultar()
      self.criar_dataframe(dados)
    with abas[1]:
      id = st.text_input("Digite o ID do livro:")
      if st.button("Consultar livro por ID"):
        dados = self.consultar_por_id(id)
        df = pd.DataFrame([dados])
        st.dataframe(df)
    with abas[2]:
      titulo = st.text_input("Digite o título do livro")
      autor = st.text_input("Digite o autor do livro")
      if st.button("Criar livro"):
        params = {
          "titulo": titulo,
          "autor": autor
        }
        retorno = self.criar(params)
        if retorno.status_code == 200:
          st.success("Livro criado com sucesso")
        else:
          st.error(retorno.text)
    with abas[3]:
      id = st.text_input("Digite o ID do livro que deseja verificar")
      if st.button("Verificar livro"):
        if not id:
          st.error("Digite o ID do livro")
        else:
          dados = self.esta_emprestado(id)
          if "emprestado" not in dados:
            st.error(dados.get("detail", "Erro ao consultar o livro"))
          elif dados["emprestado"]:
            st.warning("Este livro está EMPRESTADO")
          else:
            st.success("Este livro está DISPONÍVEL")
    super().rodape()

LivroTela().renderizar()
