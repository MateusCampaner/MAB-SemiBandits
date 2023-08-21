import unittest
from unittest.mock import patch
from MAB_Semi_Bandits import (
    Braco,
    gerar_matriz_bracos,
    gerar_recompensas,
    contar_escolhas,
    calcular_media_recompensa,
    selecionar_melhor_braco
)

class TestMultiArmedBandit(unittest.TestCase):
    def test_braco_initialization(self):
        braco = Braco(1, 10)
        self.assertTrue(1 <= braco.braco <= 10)
        self.assertEqual(braco.valor_minimo, 1)
        self.assertEqual(braco.valor_maximo, 10)
        self.assertEqual(braco.matriz_bracos, [])
        self.assertEqual(braco.contagem_escolhas, 0)
        self.assertEqual(braco.recompensas, [])

    @patch("random.randint", side_effect=[3, 6, 2, 8])
    def test_gerar_matriz_bracos(self, mock_randint):
        matriz_bracos = gerar_matriz_bracos(4, 1, 10)
        self.assertEqual(len(matriz_bracos), 4)
        self.assertEqual(matriz_bracos[0].valor_minimo, 3)
        self.assertEqual(matriz_bracos[0].valor_maximo, 6)
        self.assertEqual(matriz_bracos[1].valor_minimo, 2)
        self.assertEqual(matriz_bracos[1].valor_maximo, 8)

    @patch("random.random", side_effect=[0.2, 0.7, 0.3])
    def test_gerar_recompensas(self, mock_random):
        matriz_bracos = [Braco(1, 10), Braco(5, 15)]
        recompensas_df = gerar_recompensas(matriz_bracos, 3, 0.5, 0.3)
        self.assertEqual(recompensas_df.shape, (3, 3))

        expected_choices = [1, 2, 1]
        expected_rewards = [3, 14, 9]
        self.assertListEqual(list(recompensas_df["Braço"]), expected_choices)
        self.assertListEqual(list(recompensas_df["Recompensa"]), expected_rewards)

    def test_contar_escolhas(self):
        braco1 = Braco(1, 10)
        braco2 = Braco(5, 15)
        matriz_bracos = [braco1, braco2]
        braco1.contagem_escolhas = 3
        braco2.contagem_escolhas = 7
        escolhas = contar_escolhas(matriz_bracos)
        self.assertEqual(escolhas["Braço 1"], 3)
        self.assertEqual(escolhas["Braço 2"], 7)

    def test_calcular_media_recompensa(self):
        braco1 = Braco(1, 10)
        braco2 = Braco(5, 15)
        matriz_bracos = [braco1, braco2]
        braco1.contagem_escolhas = 3
        braco1.recompensas = [4, 8, 10]
        braco2.contagem_escolhas = 7
        braco2.recompensas = [12, 14, 16, 18, 20, 22, 24]
        medias = calcular_media_recompensa(matriz_bracos)
        self.assertEqual(medias["Braço 1"], (4 + 8 + 10) / 3)
        self.assertEqual(medias["Braço 2"], (12 + 14 + 16 + 18 + 20 + 22 + 24) / 7)

    def test_selecionar_melhor_braco(self):
        braco1 = Braco(1, 10)
        braco2 = Braco(5, 15)
        matriz_bracos = [braco1, braco2]
        braco1.contagem_escolhas = 3
        braco1.recompensas = [4, 8, 10]
        braco2.contagem_escolhas = 7
        braco2.recompensas = [12, 14, 16, 18, 20, 22, 24]
        melhor_braco_idx = selecionar_melhor_braco(matriz_bracos)
        self.assertEqual(melhor_braco_idx, 1)

if __name__ == "__main__":
    unittest.main()
