import random
import streamlit as st
import plotly.graph_objs as go
import pandas as pd

class Braco:
    def __init__(self, valor_minimo, valor_maximo):
        self.braco = random.randint(valor_minimo, valor_maximo)
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo

def gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo):
    # Criando uma matriz de bracos com valores aleatórios para o braço, valor mínimo e valor máximo
    matriz_bracos = []
    for i in range(num_bracos):
        valor_minimo = random.randint(limite_minimo, limite_maximo)
        valor_maximo = random.randint(valor_minimo, limite_maximo)
        braco = Braco(valor_minimo, valor_maximo)
        matriz_bracos.append([braco.valor_minimo, braco.braco, braco.valor_maximo])
    return matriz_bracos

def escolher_braco(medias_bracos, num_rodadas, num_bracos, epsilon):
    # Escolhendo um braço com base na estratégia Epsilon-Greedy
    if random.random() < epsilon:
        # Fase de exploração: escolhendo um braço aleatório
        braço_escolhido = random.randint(0, num_bracos-1)
    else:
        # Fase de explotação: escolhendo o braço com a maior média até o momento
        braço_escolhido = medias_bracos.index(max(medias_bracos))
    return braço_escolhido

def calcular_medias_bracos(matriz_bracos, num_bracos, num_rodadas, epsilon):
    # Calculando a média dos valores gerados por cada braço
    medias_bracos = [0] * num_bracos
    num_selecoes_bracos = [0] * num_bracos
    recompensas_bracos = [0] * num_bracos

def epsilon_greedy(medias_bracos, epsilon):
    if random.random() < epsilon:
        # Escolhe aleatoriamente um braço para explorar
        return random.randint(0, len(medias_bracos) - 1)
    else:
        # Escolhe o braço com a maior média até agora
        return max(enumerate(medias_bracos), key=lambda x: x[1])[0]

# Configurando a página do Streamlit
st.set_page_config(page_title="MAB", page_icon=":robot_face:")

# Adicionando um título
st.title("Multi Armed Bandits")

# Adicionando sliders para definir os parâmetros da matriz de robôs
num_bracos = st.slider("Número de braços:", min_value=1, max_value=20, value=5)
limite_minimo = st.slider("Limite mínimo:", min_value=0, max_value=50, value=10)
limite_maximo = st.slider("Limite máximo:", min_value=51, max_value=100, value=60)
num_rodadas = st.slider("Número de rodadas:", min_value=100, max_value=10000, value=100)
taxa_exploracao = st.slider("Taxa de exploração (%):", min_value=0, max_value=100, value=50)

# Gerando a matriz de robôs com base nos parâmetros definidos pelos sliders
matriz_bracos = gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo)

# Adicionando uma tabela com os valores mínimo e máximo de cada robô
st.write("Valores mínimo e máximo de cada braço:")
tabela_bracos = [["Braço", "Valor mínimo", "Valor máximo"]]
for i in range(num_bracos):
    tabela_bracos.append([f"Braço {i+1}", matriz_bracos[i][0], matriz_bracos[i][2]])
st.table(tabela_bracos)

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
medias_bracos = calcular_medias_bracos(matriz_bracos, num_bracos, num_rodadas, epsilon=0.1)

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