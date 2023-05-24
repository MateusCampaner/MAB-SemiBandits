import random
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.colored_header import colored_header
import plotly.graph_objects as go
import matplotlib.pyplot as plt

class Braco:
    def __init__(self, valor_minimo, valor_maximo):
        self.braco = random.randint(valor_minimo, valor_maximo)
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo
        self.matriz_bracos = []
        self.contagem_escolhas = 0
        self.recompensas = []

# Funcao pra gerar os valores dos bracos
def gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo):
    matriz_bracos = []
    for i in range(num_bracos):
        valor_minimo = random.randint(limite_minimo, limite_maximo)
        valor_maximo = random.randint(valor_minimo, limite_maximo)
        braco = Braco(valor_minimo, valor_maximo)
        matriz_bracos.append(braco)
        
    return matriz_bracos


# Funcao para gerar as recompensas e aplicar o algoritmo do MAB
def gerar_recompensas(matriz_bracos, num_rodadas, taxa_exploracao, taxa_semi):
    recompensas = []
    for i in range(num_rodadas):
        if random.random() < taxa_exploracao:
            #braco_escolhido = random.choice(matriz_bracos)
            braco_escolhido = matriz_bracos.index(random.choice(matriz_bracos))

        else:
            braco_atual = matriz_bracos[selecionar_melhor_braco(matriz_bracos)]
            if random.random() < taxa_semi:
                braco_semi = random.choice(matriz_bracos)
                if braco_semi.valor_maximo > braco_atual.valor_maximo:
                    braco_escolhido = braco_semi
                else:
                    braco_escolhido = braco_atual
            else:
                braco_escolhido = braco_atual
        
        recompensa_escolhida = random.randint(braco_escolhido.valor_minimo, braco_escolhido.valor_maximo)
        #recompensa_escolhida = random.randint(matriz_bracos[braco_escolhido].valor_minimo, matriz_bracos[braco_escolhido].valor_maximo)
        braco_escolhido.contagem_escolhas += 1
        braco_escolhido.recompensas.append(recompensa_escolhida)
        recompensas.append([f"Rodada {i + 1} ", f"Braço {braco_escolhido}", recompensa_escolhida])

    #return pd.DataFrame(recompensas, columns=["Rodada", "Braço", "Recompensa"])
    return recompensas

# Funcao para contar quantas vezes um braco foi escolhido
def contar_escolhas(matriz_bracos):
    escolhas = {}
    for i, braco in enumerate(matriz_bracos):
        escolhas[f"Braço {i+1}"] = braco.contagem_escolhas
    return escolhas

# Funcao para calcular a media das recompensas
def calcular_media_recompensa(matriz_bracos):
    medias = {}
    for i, braco in enumerate(matriz_bracos):
        media_recompensa = sum(braco.recompensas) / braco.contagem_escolhas if braco.contagem_escolhas > 0 else 0
        medias[f"Braço {i+1}"] = media_recompensa
    return medias

# Funcao para buscar o melhor braco
def selecionar_melhor_braco(matriz_bracos):
    medias_recompensas = calcular_media_recompensa(matriz_bracos)
    indice_melhor_braco = max(medias_recompensas, key=medias_recompensas.get)
    return int(indice_melhor_braco.split()[1]) - 1

#Funçao para retornar a quantidade de escolhas do melhor braço
def quantidade_escolhas_melhor_braco(matriz_bracos):
    melhor_braco = selecionar_melhor_braco(matriz_bracos)
    return matriz_bracos[melhor_braco].contagem_escolhas

# Funcao para mostrar a media do melhor braço
def selecionar_melhor_media(matriz_bracos):
    return calcular_media_recompensa(matriz_bracos)[f"Braço {melhor_braco+1}"]



# Streamlit
st.set_page_config(page_title="MAB", page_icon=":robot_face:")


st.title("Multi Armed Bandits - Semi Bandits")

colored_header(
    label="Colocar descrição aqui",
    description="Powered by UniFil",
    color_name="red-70",
)

st.sidebar.header("Escolha suas opções para o MAB")

# Parâmetros do MAB
with st.sidebar.expander("Informações de execução de algoritmo"):
    st.write('**Número de Braços:** Define o número de braços a serem executados pelo algoritmo do MAB')
    st.write('**Limite Mínimo:** Define o valor mínimo que um braço pode ser gerado')
    st.write('**Limite Máximo:** Define o valor máximo que um braço pode ser gerado')
    st.write('**Número de rodadas:** Define o número de rodadas a serem executadas pelo algoritmo do MAB')
    st.write('**Taxa de exploração:** Define a porcentagem do número de rodadas que serão utilizadas para apostar em braços aleatórios')
    st.write('**Taxa Semi Bandits:** Define a porcentagem de um braço aleatório ser escolhido após a fase de exploração')


num_bracos = st.sidebar.slider("Número de braços:", min_value=1, max_value=20, value=5)
limite_minimo = st.sidebar.slider("Limite mínimo:", min_value=0, max_value=50, value=10)
limite_maximo = st.sidebar.slider("Limite máximo:", min_value=51, max_value=100, value=60)
num_rodadas = st.sidebar.slider("Número de rodadas:", min_value=10, max_value=1000, value=100)
taxa_exploracao = st.sidebar.slider("Taxa de Exploração:", min_value=0.0, max_value=1.0, value=0.2, step=0.01)
taxa_semi = st.sidebar.slider("Taxa Semi Bandits:", min_value=0.0, max_value=1.0, value=0.2, step=0.01)


# Botão para rodar
if st.sidebar.button("Rodar MAB :game_die:"):

    # Gerando a matriz dos valores de cada braco
    matriz_bracos = gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo)

    recompensas = gerar_recompensas(matriz_bracos, num_rodadas, taxa_exploracao, taxa_semi)

    escolhas = contar_escolhas(matriz_bracos)

    fig = go.Figure(data=[go.Bar(x=list(escolhas.keys()), y=list(escolhas.values()))])

    figPie = px.pie(names=list(escolhas.keys()), values=list(escolhas.values()))

    medias_recompensas = calcular_media_recompensa(matriz_bracos)
    melhor_braco = selecionar_melhor_braco(matriz_bracos)
    qtd_melhor_braco = quantidade_escolhas_melhor_braco(matriz_bracos)
    melhor_media = selecionar_melhor_media(matriz_bracos)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Melhor Braço", value=melhor_braco+1)
    col2.metric(label="Quantidade de escolhas",value=qtd_melhor_braco)
    col3.metric(label="Media das recompensas", value=round(melhor_media, 3))


 
    
    # Print da tabela dos valores maximos e minimos
    st.write("Valores mínimo e máximo de cada braço:")
    tabela_bracos = [["Braço", "Valor mínimo", "Valor máximo"]]
    for i, braco in enumerate(matriz_bracos):
        tabela_bracos.append([f"Braço {i+1}", braco.valor_minimo, braco.valor_maximo])
    st.dataframe(tabela_bracos)

    # Gerando os valores de cada braco por rodada
    st.write("Resultados das Rodadas:")
    st.dataframe(recompensas)

    # Grafico dos valores do braco por rodada
    grafico_escolhas = pd.DataFrame(recompensas, columns=["Rodada", "Braço", "Recompensa"])
    figLine = px.line(grafico_escolhas, x="Rodada", y="Recompensa", color='Braço')
    st.write(figLine)


    # Contando as escolhas de cada braço
    st.write("Contagem de Escolhas:")
    st.dataframe(escolhas)

    # Grafico da contagem de escolha de cada braco
    fig.update_layout(
        title="Contagem de Escolhas",
        xaxis_title="Braço",
        yaxis_title="Contagem",
    )
    st.plotly_chart(fig)

    # Grafico de pizza da quantidade de escolha de cada braco
    st.plotly_chart(figPie)

    # Calculando a mé=edia das recompensas de cada braco
    
    st.write("Média das Recompensas:")
    st.dataframe(medias_recompensas)


#defender a utilizacao do mab
  