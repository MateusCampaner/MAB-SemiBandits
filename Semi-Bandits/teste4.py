import random
import streamlit as st
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

class Braco:
    def __init__(self, valor_minimo, valor_maximo):
        self.braco = random.randint(valor_minimo, valor_maximo)
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo
        self.matriz_bracos = []

def gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo):
    # Criando uma matriz de bracos com valores aleatórios para o braço, valor mínimo e valor máximo
    matriz_bracos = []
    for i in range(num_bracos):
        valor_minimo = random.randint(limite_minimo, limite_maximo)
        valor_maximo = random.randint(valor_minimo, limite_maximo)
        braco = Braco(valor_minimo, valor_maximo)
        matriz_bracos.append([braco.valor_minimo, braco.braco, braco.valor_maximo])
        
    return matriz_bracos

def gerar_recompensas(matriz_bracos, num_rodadas):
    recompensas = []
    for i in range(num_rodadas):
        
        braco_escolhido = random.choice(matriz_bracos)
        recompensa_escolhida = random.randint(braco_escolhido[0], braco_escolhido[2])
        recompensas.append([f"Rodada {i + 1} ", braco_escolhido, recompensa_escolhida])

    return pd.DataFrame(recompensas, columns=["Rodada", "Braço", "Recompensa"])



#Streamlit
st.set_page_config(page_title="MAB", page_icon=":robot_face:")

# Adicionando um título
st.title("Multi Armed Bandits - Semi Bandits")

# Parametros do MAB
num_bracos = st.sidebar.slider("Número de braços:", min_value=1, max_value=20, value=5)
limite_minimo = st.sidebar.slider("Limite mínimo:", min_value=0, max_value=50, value=10)
limite_maximo = st.sidebar.slider("Limite máximo:", min_value=51, max_value=100, value=60)
num_rodadas = st.sidebar.slider("Número de rodadas:", min_value=100, max_value=10000, value=100)

#Botão para rodar
if st.sidebar.button("Trabalhar 📈"):

    MAB = Braco(limite_minimo, limite_maximo)

    # Gerando a matriz dos valores de cada braço
    matriz_bracos = gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo)

    st.write("Valores mínimo e máximo de cada braço:")
    tabela_bracos = [["Braço", "Valor mínimo", "Valor máximo"]]
    for i in range(num_bracos):
        tabela_bracos.append([f"Braço {i+1}", matriz_bracos[i][0], matriz_bracos[i][2]])
    st.table(tabela_bracos)



    #Gerando os valores de cada braço por rodada
    valores_braco = gerar_recompensas(matriz_bracos, num_rodadas)

    recompensas = gerar_recompensas(matriz_bracos, num_rodadas)
    st.write("Resultados das Rodadas:")
    st.dataframe(recompensas)
