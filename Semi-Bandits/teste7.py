import streamlit as st
import pandas as pd
import numpy as np
import time
import random


class MultiArmedBandit:
    def __init__(self, num_bracos):
        self.num_bracos = num_bracos
        self.medias_recompensas = np.random.normal(0, 1, num_bracos)
        self.contagem_acoes = np.zeros(num_bracos)
        self.recompensas_cumulativas = np.zeros(num_bracos)

    def obter_recompensa(self, acao):
        recompensa = np.random.normal(self.medias_recompensas[acao], 1)
        self.contagem_acoes[acao] += 1
        self.recompensas_cumulativas[acao] += recompensa
        return recompensa

    def obter_melhor_braco(self):
        return np.argmax(self.medias_recompensas)

    def obter_acao_ucb(self, t):
        acoes = np.zeros(self.num_bracos)
        for i in range(self.num_bracos):
            if self.contagem_acoes[i] == 0:
                return i
            else:
                acoes[i] = (
                    self.recompensas_cumulativas[i] / self.contagem_acoes[i]
                    + np.sqrt(2 * np.log(t) / self.contagem_acoes[i])
                )
        return np.argmax(acoes)

    def obter_acao_aleatoria(self):
        return np.random.randint(self.num_bracos)

st.set_page_config(
   page_title="Contextual MAB",
   page_icon="🔫",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.snow()

st.title("Multi-Armed Bandits (MAB)")

st.sidebar.title("Configuração")
st.sidebar.selectbox('Selecione o MAB', ['Contextual'])


num_bracos = st.sidebar.number_input('Quantidade de braços', step=1, min_value=10, max_value=127)
num_passos = st.sidebar.slider('Quantidade de interações', 0, 10000, 500)

if st.sidebar.button("Calcular"):


    progress_text = "Progresso da requisição"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)

    mab = MultiArmedBandit(num_bracos)

    recompensas = np.zeros(num_passos)
    contagem_acoes = np.zeros((num_passos, num_bracos))
    recompensas_cumulativas = np.zeros((num_passos, num_bracos))

    resultados_padrao = []

    for t in range(num_passos):
        if np.random.uniform() < 0.4:
            acao = mab.obter_acao_ucb(t + 1)
        else:
            acao = mab.obter_acao_aleatoria()

        recompensa = mab.obter_recompensa(acao)

        recompensas[t] = recompensa
        contagem_acoes[t] = mab.contagem_acoes
        recompensas_cumulativas[t] = mab.recompensas_cumulativas

        # Salvar os resultados em sequência na lista
        resultados_padrao.append({
            'Interação': t + 1,
            'Recompensa dos braços escolhidos': recompensa,
            'Contagem de escolhas por braço': mab.contagem_acoes.copy(),
            'Soma da recompensa por braço': mab.recompensas_cumulativas.copy()
        })

    melhor_braco = mab.obter_melhor_braco()
    recompensas_melhor_braco = recompensas_cumulativas[:, melhor_braco]


    chart_data = pd.DataFrame(recompensas_cumulativas, columns=[f'Braço {i+1}' for i in range(num_bracos)])

    st.subheader("Desempenho dos Braços")
    st.line_chart(chart_data)

    # Configurar os dados para o gráfico de linha
    chart_data_line = pd.DataFrame(recompensas_melhor_braco, columns=['Soma das recompenças'])

    # Converter a lista de resultados em um DataFrame
    df_resultados = pd.DataFrame(resultados_padrao)
    st.subheader("Tabela de Resultados")
    st.dataframe(df_resultados)


    melhor_braco_numero = melhor_braco + 1
    st.subheader(f"Desempenho do Braço {melhor_braco_numero}")
    st.line_chart(chart_data_line)