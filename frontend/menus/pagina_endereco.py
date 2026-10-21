import streamlit as st
from componentes.base_tela import TelaBase
from connection.base_api import BaseAPI
import pandas as pd

class EnderecoTela(TelaBase):

  def __init__(self):
    self.base = BaseAPI()
    self.titulo = "Tela de Endereço"
    self.descricao = "Essa tela é usada para consultar endereços"

  def consultar(self):
    endpoint = "/enderecos/pegar-dados-endereco"
    dados = self.base.get(endpoint)
    return dados
  
  def consultar_por_id(self, id):
    endpoint = f"/enderecos/pegar-dados-endereco-por-id/{id}"
    dados = self.base.get(endpoint)
    return dados

  def criar_dataframe(self, dados):
    df = pd.DataFrame(dados)
    st.dataframe(df)

  def renderizar(self):
    super().cabecalho(self.titulo, self.descricao)
    abas = st.tabs(["Consultar todos", "Consultar por ID", "Criar Endereço", "Atualizar Endereço", "Deletar Endereço"])
    with abas[0]:
      dados = self.consultar()
      self.criar_dataframe(dados)
    with abas[1]:
      id = st.text_input("Digite o ID do endereço:")
      if id:
        id = int(id)
        dados = self.consultar_por_id(id)
        self.criar_dataframe(dados)
    with abas[2]:
      pass
    with abas[3]:
      pass
    with abas[4]:
      pass
    super().rodape()

EnderecoTela().renderizar()