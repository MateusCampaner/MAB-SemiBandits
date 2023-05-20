import random
import streamlit as st
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

class Braco:

    def __init__(self, num_bracos):
        self.num_bracos = num_bracos
        valor_minimo = 0
        valor_maximo = 100
        self.braco = random.randint(valor_minimo, valor_maximo)
        self.matriz_bracos = []

    def gerar_matriz_bracos(self, limite_minimo, limite_maximo):
    # Criando uma matriz de bracos com valores aleatórios para o braço, valor mínimo e valor máximo
        matriz_bracos = []
        for i in range(self.num_bracos):
            valor_minimo = random.randint(limite_minimo, limite_maximo)
            valor_maximo = random.randint(valor_minimo, limite_maximo)
            braco = Braco(valor_minimo, valor_maximo)
            matriz_bracos.append([braco.braco])

        return matriz_bracos
    
    def gerar_recompensa(ind):
        recompensa = random.randint(braco)

    def escolhe_braco(num_bracos):
        braco_escolhido = random.randint(0,num_bracos)
        recompensa = random.choice(matriz_bracos[braco_escolhido])

        return braco_escolhido

    def gerar_valores_braco(matriz_bracos, num_rodadas):
        # Rodando os valores para cada rodada
        
        for i in range(num_bracos):
            valores_gerados = []
            valor_minimo = random.randint(limite_minimo, limite_maximo)
            valor_maximo = random.randint(valor_minimo, limite_maximo)
            braco_escolhido = random.randint(valor_minimo, valor_maximo)
            recompensa_rodada = random.randint
            valores_gerados.append([braco_escolhido, recompensa_rodada])

        return valores_gerados

    def calcular_medias_bracos(matriz_bracos, num_bracos, num_rodadas):
        # Calculando a média dos valores gerados por cada braco
        medias_bracos = []
        for i in range(num_rodadas):
            media_braco = sum(gerar_valores_braco) / len(gerar_valores_braco)
            medias_bracos.append(media_braco)
        return medias_bracos

# Configurando a página do Streamlit
st.set_page_config(page_title="MAB", page_icon=":robot_face:")

# Adicionando um título
st.title("Multi Armed Bandits")

# Adicionando sliders para definir os parâmetros da matriz de robôs
num_bracos = st.sidebar.slider("Número de braços:", min_value=1, max_value=20, value=5)
limite_minimo = st.sidebar.slider("Limite mínimo:", min_value=0, max_value=50, value=10)
limite_maximo = st.sidebar.slider("Limite máximo:", min_value=51, max_value=100, value=60)
num_rodadas = st.sidebar.slider("Número de rodadas:", min_value=100, max_value=10000, value=100)

if st.sidebar.button("Trabalhar 📈"):

    MAB = Braco(num_bracos)

    # Gerando a matriz de robôs com base nos parâmetros definidos pelos sliders
    matriz_bracos = MAB.gerar_matriz_bracos(num_bracos)

    # Adicionando uma tabela com os valores mínimo e máximo de cada robô
    st.write("Valores mínimo e máximo de cada braço:")
    tabela_bracos = [["Braço", "Valor mínimo", "Valor máximo"]]
    for i in range(num_bracos):
        tabela_bracos.append([f"Braço {i+1}", matriz_bracos[i][0], matriz_bracos[i][2]])
    st.table(tabela_bracos)

    #Gerando os valores de cada braço por rodada
    valores_braco = gerar_valores_braco(num_bracos, matriz_bracos, num_rodadas)

    st.write("Resultados das rodadas:")
    tabela_resultados = [["Rodada", "Braço", "Recompensa"]]
    for i in range(num_rodadas):
        braco_escolhido = gerar_valores_braco(matriz_bracos, num_rodadas)
        recompensa_braco = gerar_valores_braco(matriz_bracos, num_rodadas)
        tabela_resultados.append([f"Rodada {i+1}", braco_escolhido, recompensa_braco])
    st.table(tabela_resultados)

    # Realizando as rodadas para cada robô e mostrando os resultados em uma tabela
    st.write("Resultados das rodadas:")
    tabela_resultados = [["Braço"]]
    for i in range(num_bracos):
        valores_gerados = []
        numero_aleatorio = random.randint(matriz_bracos[i][0], matriz_bracos[i][2])
        valores_gerados.append(numero_aleatorio)
        tabela_resultados.append([f"Braço {i+1}"] + valores_gerados)
    st.table(tabela_resultados)

    # Realizando as rodadas para cada robô e mostrando os resultados em uma tabela
    st.write("Resultados das rodadas:")
    tabela_resultados = [["Braço"]]
    for i in range(num_bracos):
        valores_gerados = []
        for j in range(num_rodadas):
            numero_aleatorio = random.randint(matriz_bracos[i][0], matriz_bracos[i][2])
            valores_gerados.append(numero_aleatorio)
        tabela_resultados.append([f"Braço {i+1}"] + valores_gerados)
    st.table(tabela_resultados)

    # Calculando as médias dos valores gerados por cada robô
    medias_bracos = calcular_medias_bracos(matriz_bracos, num_bracos, num_rodadas)

    # Mostrando as médias em uma tabela
    st.write("Médias dos valores gerados por cada braço:")
    tabela_medias = [["Braço", "Média"]]
    for i in range(num_bracos):
        tabela_medias.append([f"Braço {i+1}", medias_bracos[i]])
    st.table(tabela_medias)

    bar_chart = go.AngularAxis(x=[f'Braços {i+1}' for i in range(num_bracos)], y=medias_bracos, name='Média')
    layout = go.Layout(title='Médias dos valores gerados por cada braço', xaxis=dict(title='Braço'), yaxis=dict(title='Média'))
    fig = go.Figure(data=[bar_chart], layout=layout)
    st.plotly_chart(fig)

    df = pd.DataFrame(
        medias_bracos,columns=['Braço', 'Média']
    )

    pie_chart = px.medias_bracos
    fig = px.pie(df, values='Média', names='Braço')
    st.write(fig)
