import streamlit as st
import numpy as np
import random

# Configuração do Streamlit
st.title("Simulação de Multi-Armed Bandit")
num_bracos = st.slider("Número de Braços:", min_value=2, max_value=10, value=5)
num_rodadas = st.slider("Número de Rodadas:", min_value=1, max_value=1000, value=100)
epsilon = st.slider("Valor de Epsilon:", min_value=0.0, max_value=1.0, value=0.1)

# Inicialização dos valores iniciais de cada braço
valores_iniciais = [random.random() for _ in range(num_bracos)]
num_selecoes = [0] * num_bracos
recompensas = [0] * num_bracos

# Função para seleção de um braço
def selecionar_braco():
    if random.random() < epsilon:
        return random.randint(0, num_bracos - 1)
    else:
        valores_medios = [recompensas[i] / num_selecoes[i] if num_selecoes[i] > 0 else 0 for i in range(num_bracos)]
        return np.argmax(valores_medios)

# Simulação das rodadas
for rodada in range(num_rodadas):
    braco_selecionado = selecionar_braco()
    recompensa = random.random()  # Simulação de uma recompensa aleatória
    num_selecoes[braco_selecionado] += 1
    recompensas[braco_selecionado] += recompensa

# Exibição dos resultados
st.write("Valores Iniciais:")
tabela_valores = np.array(valores_iniciais).reshape(-1, 1)
st.dataframe(tabela_valores, width=150)

st.write("Número de Seleções:")
tabela_selecoes = np.array(num_selecoes).reshape(-1, 1)
st.dataframe(tabela_selecoes, width=150)

st.write("Recompensas Totais:")
tabela_recompensas = np.array(recompensas).reshape(-1, 1)
st.dataframe(tabela_recompensas, width=150)