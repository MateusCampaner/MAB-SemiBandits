import random
import streamlit as st
import plotly.graph_objs as go

class Braco:
    def __init__(self, valor_minimo, valor_maximo):
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo

    def girar_braco(self):
        return random.randint(self.valor_minimo, self.valor_maximo)

class MAB:
    def __init__(self, num_bracos, limite_minimo, limite_maximo, num_rodadas):
        self.num_bracos = num_bracos
        self.limite_minimo = limite_minimo
        self.limite_maximo = limite_maximo
        self.num_rodadas = num_rodadas

        self.matriz_bracos = self.gerar_matriz_bracos()
        self.medias_bracos = [0] * num_bracos
        self.num_jogadas_bracos = [0] * num_bracos

    def gerar_matriz_bracos(self):
        # Criando uma matriz de bracos com valores aleatórios para o braço, valor mínimo e valor máximo
        matriz_bracos = []
        for i in range(self.num_bracos):
            valor_minimo = random.randint(self.limite_minimo, self.limite_maximo)
            valor_maximo = random.randint(valor_minimo, self.limite_maximo)
            braco = Braco(valor_minimo, valor_maximo)
            matriz_bracos.append(braco)
        return matriz_bracos

    def jogar(self):
        # Escolhendo o braço com a maior média de valores gerados
        idx_braco_escolhido = self.medias_bracos.index(max(self.medias_bracos))
        braco_escolhido = self.matriz_bracos[idx_braco_escolhido]
        
        # Girando o braço escolhido
        valor_gerado = braco_escolhido.girar_braco()
        
        # Atualizando as estatísticas do braço escolhido
        self.num_jogadas_bracos[idx_braco_escolhido] += 1
        self.medias_bracos[idx_braco_escolhido] = ((self.medias_bracos[idx_braco_escolhido] * (self.num_jogadas_bracos[idx_braco_escolhido] - 1)) + valor_gerado) / self.num_jogadas_bracos[idx_braco_escolhido]
        
        # Retornando o valor gerado e a matriz de estatísticas
        return valor_gerado, self.medias_bracos, self.num_jogadas_bracos