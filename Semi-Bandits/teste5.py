import random
import streamlit as st
import plotly.graph_objs as go
import math

import random
import streamlit as st
import plotly.graph_objs as go
import math

class Braco:
    def __init__(self, valor_minimo, valor_maximo):
        self.braco = random.randint(valor_minimo, valor_maximo)
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo


class MAB:
    def __init__(self, num_bracos, limite_minimo, limite_maximo):
        self.matriz_bracos = self.gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo)
        self.num_bracos = num_bracos
        self.limite_minimo = limite_minimo
        self.limite_maximo = limite_maximo
        self.tabela_medias = []
        self.medias_bracos = []

    def gerar_matriz_bracos(self, num_bracos, limite_minimo, limite_maximo):
        # Criando uma matriz de bracos com valores aleatórios para o braço, valor mínimo e valor máximo
        matriz_bracos = []
        for i in range(num_bracos):
            valor_minimo = random.randint(limite_minimo, limite_maximo)
            valor_maximo = random.randint(valor_minimo, limite_maximo)
            braco = Braco(valor_minimo, valor_maximo)
            matriz_bracos.append([braco.valor_minimo, braco.braco, braco.valor_maximo])
        return matriz_bracos

    def selecionar_braco(self):
        if random.random() < self.taxa_exploracao/100:
            return random.randint(0, self.num_bracos - 1)
        else:
            return self.medias_bracos.index(max(self.medias_bracos))

    def realizar_rodada(self):
        braco_escolhido = self.selecionar_braco()
        numero_aleatorio = random.randint(self.matriz_bracos[braco_escolhido][0], self.matriz_bracos[braco_escolhido][2])
        self.medias_bracos[braco_escolhido] = (self.medias_bracos[braco_escolhido]*self.num_rodadas + numero_aleatorio) / (self.num_rodadas + 1)
        self.tabela_medias = [["Braço", "Média"]]
        for i in range(self.num_bracos):
            self.tabela_medias.append([f"Braço {i+1}", self.medias_bracos[i]])

    def rodar(self, num_rodadas, taxa_exploracao):
        self.num_rodadas = num_rodadas
        self.taxa_exploracao = taxa_exploracao
        self.medias_bracos = [0] * self.num_bracos
        for i in range(self.num_rodadas):
            self.realizar_rodada()

    def mostrar_medias(self):
        st.write("Médias dos valores gerados por cada braço:")
        st.table(self.tabela_medias)

# Componentes da interface
# Adicionando sliders para definir os parâmetros da matriz de robôs
num_bracos = st.slider("Número de braços:", min_value=1, max_value=20, value=5)
limite_minimo = st.slider("Limite mínimo:", min_value=0, max_value=50, value=10)
limite_maximo = st.slider("Limite máximo:", min_value=51, max_value=100, value=60)
num_rodadas = st.slider("Número de rodadas:", min_value=100, max_value=10000, value=100)
taxa_exploracao = st.slider("Taxa de exploração (%):", min_value=0, max_value=100, value=50)

st.subheader("Resultados da simulação")

st.write(f"Total de rodadas: {num_rodadas}")
st.write(f"Taxa de exploração: {taxa_exploracao}%")
st.write("")

tabela_resultados = [["Braço", "Valor mínimo", "Valor máximo", "Média"]]
for i in range(MAB.num_bracos):
    braço = MAB.matriz_bracos[i]
    media = round(MAB.medias_bracos[i], 2)
    tabela_resultados.append([f"Braço {i+1}", braço[0], braço[2], media])

    st.table(tabela_resultados)

    fig = go.Figure()
    for i in range(MAB.num_bracos):
        fig.add_trace(go.Scatter(x=list(range(1, num_rodadas+1)), y=MAB.medias_bracos[i], name=f"Braço {i+1}"))

    fig.update_layout(
        title={
            'text': "Evolução das médias dos braços",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Número de rodadas",
        yaxis_title="Média",
        legend_title="Braços",
        width=800,
        height=500
    )

