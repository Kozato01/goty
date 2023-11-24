import pandas as pd
import streamlit as st

def obter_pontos_por_categoria(categoria):
    # Definir a pontuação para cada categoria (ajuste conforme necessário)
    pontuacao_por_categoria = {
        "Jogo do Ano - 10 pontos": 10,
        "Melhor Direção de Jogo - 5 pontos": 5,
        "Melhor Narrativa - 5 pontos": 5,
        "Melhor Direção de Arte - 5 pontos": 5,
        "Melhor Trilha Sonora - 5 pontos": 5,
        "Melhor Design de Áudio - 5 pontos": 5,
        "Melhor Atuação - 5 pontos": 5,
        "Inovação em Acessibilidade - 5 pontos": 5,
        "Jogos com Maior Impacto Social - 5 pontos": 5,
        "Melhor Jogo Contínuo - 5 pontos": 5,
        "Melhor Suporte Comunitário - 3 pontos": 3,
        "Melhor Jogo Independente - 3 pontos": 3,
        "Melhor Estreia de um Estúdio Indie - 3 pontos": 3,
        "Melhor Jogo Mobile - 3 pontos": 3,
        "Melhor VR / AR - 3 pontos": 3,
        "Melhor Jogo de Ação - 3 pontos": 3,
        "Melhor Jogo de Ação / Aventura - 3 pontos": 3,
        "Melhor RPG - 3 pontos": 3,
        "Melhor Jogo de Luta - 3 pontos": 3,
        "Melhor Jogo para Família - 3 pontos": 3,
        "Melhor Jogo de Simulação / Estratégia - 2 pontos": 2,
        "Melhor Jogo de Esporte / Corrida - 2 pontos": 2,
        "Melhor Jogo Multiplayer - 2 pontos": 2,
        "Melhor Adaptação - 2 pontos": 2,
        "Jogo Mais Aguardado de 2024 - 2 pontos": 2,
    }

    return pontuacao_por_categoria.get(categoria, 0)