import random
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.colored_header import colored_header
import plotly.graph_objects as go
import plotly.express as px
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
            braco_escolhido_idx = random.choice(range(len(matriz_bracos)))
        else:
            braco_atual_idx = selecionar_melhor_braco(matriz_bracos)
            if random.random() < taxa_semi:
                melhores_bracos = int(len(matriz_bracos) * taxa_semi)
                braco_semi_idx = random.choice(range(len(matriz_bracos[:melhores_bracos])))
                if matriz_bracos[braco_semi_idx].valor_maximo > matriz_bracos[braco_atual_idx].valor_maximo:
                    braco_escolhido_idx = braco_semi_idx
                else:
                    braco_escolhido_idx = braco_atual_idx
            else:
                braco_escolhido_idx = braco_atual_idx
        
        braco_escolhido = braco_escolhido_idx + 1  # Adiciona 1 para corresponder ao número do braço
        recompensa_escolhida = random.randint(matriz_bracos[braco_escolhido_idx].valor_minimo, matriz_bracos[braco_escolhido_idx].valor_maximo)
        matriz_bracos[braco_escolhido_idx].contagem_escolhas += 1
        matriz_bracos[braco_escolhido_idx].recompensas.append(recompensa_escolhida)
        recompensas.append([f"Rodada {i + 1} ", braco_escolhido, recompensa_escolhida])

    return pd.DataFrame(recompensas, columns=["Rodada", "Braço", "Recompensa"])

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

colored_header(
    label="",
    description="",
    color_name="red-70",
)

st.title("Multi Armed Bandits - Semi Bandits")

colored_header(
    label="",
    description="",
    color_name="red-70",
)

st.sidebar.header("Escolha suas opções para o MAB")
# Informação sopbre o MAB Semi-Bandits
with st.sidebar.expander("Informações sobre o MAB Semi-Bandits"):
    st.write("O **MAB Semi-Bandits** é um algoritmo onde o objetivo é encontrar um braço que traga as melhores recompensas")
    st.write("Para isso o algoritmo é divido em duas fases **Exploração** e **Extração**")
    st.write("Durante a **Exploração** o algoritmo escolhe os braços aleatoriamente e gera recompensas para eles")
    st.write("Após isso é escolhido o braço que deu as melhores recompensas para a fase de **Extração**")
    st.write("Durante a fase de **Extração** é escolhido o melhor braço para se gerar as recompensas")
    st.write("Enquanto esse melhor braço é executado há uma porcentagem definida pela **Taxa Semi-Bandits** de outro braço ser escolhido para se apostar")
    st.write("Porém esse braço escolhido não é aleatorio, ele é escolhido com base nos braços que tiveram bom desempenho durante a fase de exploração")
    st.write("São escolhidos os melhores braços pois eles tiveram um desempenho pior que o melhor braço escolhido, mas não tiveram as piores recompensas")
    st.write("È feito essa aposta durante a fase de Extração, pois é necessário para saber se o braço escolhido é o que está trazendo as melhores recompensas")

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
if st.sidebar.button("Executar algoritmo MAB :game_die:"):

    # Gerando a matriz dos valores de cada braco
    matriz_bracos = gerar_matriz_bracos(num_bracos, limite_minimo, limite_maximo)

    recompensas = gerar_recompensas(matriz_bracos, num_rodadas, taxa_exploracao, taxa_semi)

    escolhas = contar_escolhas(matriz_bracos)

    figBarContagem = go.Figure(data=[go.Bar(x=list(escolhas.keys()), y=list(escolhas.values()))])

    figPieContagem = px.pie(names=list(escolhas.keys()), values=list(escolhas.values()))

    medias_recompensas = calcular_media_recompensa(matriz_bracos)

    figBarMedias = go.Figure(data=[go.Bar(x=list(medias_recompensas.keys()), y=list(medias_recompensas.values()))])

    melhor_braco = selecionar_melhor_braco(matriz_bracos)
    qtd_melhor_braco = quantidade_escolhas_melhor_braco(matriz_bracos)
    melhor_media = selecionar_melhor_media(matriz_bracos)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Melhor Braço", value=melhor_braco+1)
    col2.metric(label="Quantidade de escolhas",value=qtd_melhor_braco)
    col3.metric(label="Media das recompensas", value=round(melhor_media, 3))

    colored_header(
    label="",
    description="",
    color_name="red-70",
    )

    # Print da tabela dos valores minimos e maximos 
    st.header("Braços gerados")
    st.write("Tabelas dos Valores mínimos e máximos de cada braço gerado")
    tabela_bracos = [["Braço", "Valor mínimo", "Valor máximo"]]
    for i, braco in enumerate(matriz_bracos):
        tabela_bracos.append([f"Braço {i+1}", braco.valor_minimo, braco.valor_maximo])
    st.table(tabela_bracos)

    # Grafico de barras dos valores minimos e maximos
    dados_bracos = []
    for i, braco in enumerate(matriz_bracos):
        dados_braco = {'Braço': f"Braço {i+1}", 'Valor Mínimo': braco.valor_minimo, 'Valor Máximo': braco.valor_maximo}
        dados_bracos.append(dados_braco)
    st.write("Gráfico dos Valores mínimos e máximos de cada braço gerado")
    st.bar_chart(dados_bracos, x='Braço', y=['Valor Mínimo', 'Valor Máximo'])

    # Gerando os valores de cada braco por rodada
    st.header("Resultado das rodadas")
    st.write("Tabelas com os resultados dos braços por rodada")
    st.dataframe(recompensas)

    st.write("Gráfico de dispersão dos resultados de cada rodada")
    df = recompensas
    fig = px.scatter(
        df,
        x="Rodada",
        y="Recompensa",
        color="Braço",
        color_continuous_scale="reds"   
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    # Contando as escolhas de cada braços
    st.header("Contagem de Escolhas")
    st.write("Tabela da contagem de escolhas de cada braço")
    st.table(escolhas)

    # Grafico da contagem de escolha de cada braco
    figBarContagem.update_layout(
        title="Gráfico de barras da contagem de escolhas de cada braço",
        xaxis_title="Braço",
        yaxis_title="Contagem",
    )
    st.plotly_chart(figBarContagem)

    # Grafico de pizza da quantidade de escolha de cada braco
    figPieContagem.update_layout(
        title="Gráfico de pizza da contagem de escolhas de cada braço",
        xaxis_title="Braço",
        yaxis_title="Contagem",
    )
    st.plotly_chart(figPieContagem)

    # Calculando a méedia das recompensas de cada braco
    st.header("Média das recompensas")
    st.write("Tabela da Média das recompensas")
    st.table(medias_recompensas)

    # Grafico da contagem de escolha de cada braco
    figBarMedias.update_layout(
        title="Gráfico de barras da média de cada braço",
        xaxis_title="Braço",
        yaxis_title="Contagem",
    )
    st.plotly_chart(figBarMedias)

   

  