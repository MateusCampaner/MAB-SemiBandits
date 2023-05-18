#streamlit
import streamlit as st
import numpy as np
import random


class Bracos:
    def __init__(self, recompensa_minima=None, recompensa_maxima=None):
        self.braco = random.randint(recompensa_minima, recompensa_maxima)
        self.recompensa_minima = recompensa_minima
        self.recompensa_maxima = recompensa_maxima


    def puxar_braco(self, braco):
        return np.random.normal(self.recompensa[braco])




def ucb_bandit(num_bracos, num_passos, medias_recompensa, desvios_padrao_recompensa, c):
    
    num_escolhas = np.zeros(num_bracos)
    recompensa_total = 0

    for i in range(num_bracos):
        recompensa = np.random.normal(medias_recompensa[i], desvios_padrao_recompensa[i])
        recompensa_total += recompensa
        num_escolhas[i] += 1

    for i in range(num_bracos, num_passos):
        ucb_valores = medias_recompensa + c * np.sqrt(np.log(i) / (num_escolhas + 1e-6))

        braço_a_escolher = np.argmax(ucb_valores)

        recompensa = np.random.normal(medias_recompensa[braço_a_escolher], desvios_padrao_recompensa[braço_a_escolher])
        recompensa_total += recompensa
        num_escolhas[braço_a_escolher] += 1
        medias_recompensa[braço_a_escolher] = ((num_escolhas[braço_a_escolher] - 1) * medias_recompensa[braço_a_escolher] + recompensa) / num_escolhas[braço_a_escolher]

    return recompensa_total


st.title("Algoritmo UCB para o MAB semi-bandits")

num_bracos = st.slider("Número de braços", min_value=2, max_value=10, value=5, step=1)
num_passos = st.slider("Número de passos", min_value=100, max_value=10000, value=1000, step=100)
desvio_padrao = st.slider("Desvio padrão da recompensa", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
c = st.slider("Parâmetro de exploração C", min_value=0.1, max_value=5.0, value=2.0, step=0.1)

medias_recompensa = np.random.normal(0, desvio_padrao, num_bracos)
desvios_padrao_recompensa = np.ones(num_bracos)

recompensa_total = ucb_bandit(num_bracos, num_passos, medias_recompensa, desvios_padrao_recompensa, c)
st.write(f"Recompensa total: {recompensa_total}")