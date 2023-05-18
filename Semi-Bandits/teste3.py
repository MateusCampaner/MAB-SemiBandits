import random
import streamlit as st

class Robo:
    def __init__(self, limite_minimo, limite_maximo):
        self.valor_minimo = random.randint(limite_minimo, limite_maximo)
        self.valor_maximo = random.randint(self.valor_minimo, limite_maximo)
        self.braco = random.randint(self.valor_minimo, self.valor_maximo)

def gerar_matriz_bracos(num_robos, limite_minimo, limite_maximo):
    # Criando uma matriz de robôs com valores aleatórios para o braço, valor mínimo e valor máximo
    matriz_bracos = []
    for i in range(num_robos):
        robo = Robo(limite_minimo, limite_maximo)
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
rodadas = st.slider("Número de rodadas:", min_value=1, max_value=10, value=5)

# Gerando a matriz de robôs com base nos parâmetros definidos pelos sliders
matriz_bracos = gerar_matriz_bracos(num_robos, limite_minimo, limite_maximo)

# Adicionando uma tabela com os valores mínimo e máximo de cada robô
st.write("Valores mínimo e máximo de cada robô:")
tabela_robos = [["Robô", "Valor mínimo", "Valor máximo"]]
for i in range(num_robos):
    tabela_robos.append([f"Robô {i+1}", matriz_bracos[i][0], matriz_bracos[i][2]])
st.table(tabela_robos)

# Realizando as rodadas para gerar números aleatórios e calcular a média
for i in range(rodadas):
    soma_numeros_aleatorios = [0] * num_robos # Lista para armazenar a soma dos números aleatórios gerados para cada robô
    for j in range(num_robos):
        numero_aleatorio = random.randint(matriz_bracos[j][0], matriz_bracos[j][2])
        soma_numeros_aleatorios[j] += numero_aleatorio # Adicionando o número aleatório gerado na soma correspondente ao robô
        st.write(f"Robô {j+1} gerou o número {numero_aleatorio}")
    for j in range(num_robos):
        media_aleatorios = soma_numeros_aleatorios[j] / rodadas # Calculando a média dos números aleatórios gerados para cada robô
        st.write(f"Média de números aleatórios gerados para o robô {j+1}: {media_aleatorios}")