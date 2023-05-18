import random
import streamlit as st

class Robo:
    def __init__(self, valor_minimo, valor_maximo):
        self.braco = random.randint(valor_minimo, valor_maximo)
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo

def gerar_matriz_bracos(num_robos, limite_minimo, limite_maximo):
    # Criando uma matriz de robôs com valores aleatórios para o braço, valor mínimo e valor máximo
    matriz_bracos = []
    for i in range(num_robos):
        valor_minimo = random.randint(limite_minimo, limite_maximo)
        valor_maximo = random.randint(valor_minimo, limite_maximo)
        robo = Robo(valor_minimo, valor_maximo)
        matriz_bracos.append([robo.valor_minimo, robo.braco, robo.valor_maximo])
    return matriz_bracos

# Configurando a página do Streamlit
st.set_page_config(page_title="Matriz de Robôs", page_icon=":robot_face:")

# Adicionando um título
st.title("Matriz de Robôs")

# Adicionando sliders para definir os parâmetros da matriz de robôs
num_robos = st.slider("Número de robôs:", min_value=1, max_value=20, value=5)
limite_minimo = st.slider("Limite mínimo:", min_value=0, max_value=50, value=10)
limite_maximo = st.slider("Limite máximo:", min_value=51, max_value=100, value=60)

# Gerando a matriz de robôs com base nos parâmetros definidos pelos sliders
matriz_bracos = gerar_matriz_bracos(num_robos, limite_minimo, limite_maximo)

# Exibindo a matriz de robôs gerada na tela
st.write("Matriz de robôs gerada:")
for i in range(num_robos):
    st.write(matriz_bracos[i])