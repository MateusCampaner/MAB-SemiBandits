import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dados para o gráfico
dados = {
    'Braço': ['Braço 1', 'Braço 2', 'Braço 3', 'Braço 4'],
    'Valor mínimo': [10, 15, 12, 8],
    'Valor máximo': [20, 25, 18, 16]
}

# Criando um DataFrame com os dados
df = pd.DataFrame(dados)

# Configurando o cabeçalho e a tabela no Streamlit
st.header("Braços gerados")
st.write("Tabelas dos Valores mínimos e máximos de cada braço gerado")
st.table(df)

# Criando o gráfico de barras
fig, ax = plt.subplots()
ax.bar(df['Braço'], df['Valor mínimo'], label="Valor mínimo")
ax.bar(df['Braço'], df['Valor máximo'], label="Valor máximo")
ax.set_xlabel("Braço")
ax.set_ylabel("Valor")
ax.set_title("Valores mínimos e máximos de cada braço gerado")
ax.legend()

# Exibindo o gráfico no Streamlit
st.pyplot(fig)