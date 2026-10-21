import streamlit as st
from connection.base_api import BaseAPI
import pandas as pd

base = BaseAPI()
id = st.text_input("ID do Aluno")
id = int(id)

endpoint = f"/alunos/pegar-dados-alunos-por-id/{id}"
dados = base.get(endpoint)

df = pd.DataFrame(dados)
st.dataframe(df)