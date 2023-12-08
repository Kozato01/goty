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


def obter_categorias_escolhidas():
    return {
    1: {"Categoria": "Jogo do Ano - 10 pontos", "Opções": ["Alan Wake 2", "Baldur's Gate 3", "Marvel's Spider-Man 2", "Resident Evil 4 Remake", "Super Mario Bros. Wonder", "The Legend of Zelda: Tears of the Kingdom"]},
    2: {"Categoria": "Melhor Direção de Jogo - 5 pontos", "Opções": ["Alan Wake 2", "Baldur's Gate 3", "Marvel's Spider-Man 2", "Super Mario Bros. Wonder", "The Legend of Zelda: Tears of the Kingdom"]},
    3: {"Categoria": "Melhor Narrativa - 5 pontos", "Opções": ["Alan Wake 2", "Baldur's Gate 3", "Cyberpunk 2077: Phantom Liberty", "Final Fantasy XVI", "Marvel's Spider-Man 2"]},
    4: {"Categoria": "Melhor Direção de Arte - 5 pontos", "Opções": ["Alan Wake 2", "Hi-Fi Rush", "Lies of P", "Super Mario Bros. Wonder", "The Legend of Zelda: Tears of the Kingdom"]},
    5: {"Categoria": "Melhor Trilha Sonora - 5 pontos", "Opções": ["Alan Wake 2, por Petri Alanko", "Baldur's Gate 3, por Borislav Slavov", "Final Fantasy XVI, por Masayoshi Soken", "Hi-Fi Rush, por Shuichi Kobori", "The Legend of Zelda: Tears of the Kingdom, por Nintendo Sound Team"]},
    6: {"Categoria": "Melhor Design de Áudio - 5 pontos", "Opções": ["Alan Wake 2", "Dead Space", "Marvel's Spider-Man 2", "Hi-Fi Rush", "Resident Evil 4 Remake"]},
    7: {"Categoria": "Melhor Atuação - 5 pontos", "Opções": ["Ben Starr, por Final Fantasy XVI", "Cameron Monaghan, por Star Wars Jedi: Survivor", "Idris Elba, por Cyberpunk 2077: Phantom Liberty", "Melanie Liburd, por Alan Wake 2", "Neil Newbon, por Baldur's Gate 3", "Yuri Lowenthal, por Marvel's Spider-Man 2"]},
    8: {"Categoria": "Inovação em Acessibilidade - 5 pontos", "Opções": ["Diablo IV", "Forza Motorsport", "Hi-Fi Rush", "Marvel's Spider-Man 2", "Mortal Kombat 1", "Street Fighter 6"]},
    9: {"Categoria": "Jogos com Maior Impacto Social - 5 pontos", "Opções": ["A Space for the Unbound", "Chants of Sennaar", "Goodbye Volcano High", "Tchia", "Terra Nil", "Venba"]},
    10: {"Categoria": "Melhor Jogo Contínuo - 5 pontos", "Opções": ["Apex Legends", "Cyberpunk 2077", "Final Fantasy XIV", "Fortnite", "Genshin Impact"]},
    11: {"Categoria": "Melhor Suporte Comunitário - 3 pontos", "Opções": ["Baldur's Gate 3", "Cyberpunk 2077", "Destiny 2", "Final Fantasy XIV", "No Man's Sky"]},
    12: {"Categoria": "Melhor Jogo Independente - 3 pontos", "Opções": ["Coccoon", "Dave the Diver", "Dredge", "Sea of Stars", "Viewfinder"]},
    13: {"Categoria": "Melhor Estreia de um Estúdio Indie - 3 pontos", "Opções": ["Coccoon", "Dredge", "Pizza Tower", "Venba", "Viewfinder"]},
    14: {"Categoria": "Melhor Jogo Mobile - 3 pontos", "Opções": ["Final Fantasy VII: Ever Crisis", "Hello Kitty Island Adventure", "Honkai: Star Rail", "Monster Hunter Now", "Terra Nil"]},
    15: {"Categoria": "Melhor VR / AR - 3 pontos", "Opções": ["Gran Turismo 7", "Horizon Call of the Mountain", "Humanity", "Resident Evil Village VR Mode", "Synapse"]},
    16: {"Categoria": "Melhor Jogo de Ação - 3 pontos", "Opções": ["Armored Core VI: Fires of Rubicorn", "Dead Island 2", "Ghostrunner 2", "Hi-Fi Rush", "Remnant 2"]},
    17: {"Categoria": "Melhor Jogo de Ação / Aventura - 3 pontos", "Opções": ["Alan Wake 2", "Marvel's Spider-Man 2", "Resident Evil 4 Remake", "Star Wars Jedi: Survivor", "The Legend of Zelda: Tears of the Kingdom"]},
    18: {"Categoria": "Melhor RPG - 3 pontos", "Opções": ["Baldur's Gate 3", "Final Fantasy XVI", "Lies of P", "Sea of Stars", "Starfield"]},
    19: {"Categoria": "Melhor Jogo de Luta - 3 pontos", "Opções": ["God of Rock", "Mortal Kombat 1", "Nickelodeon All-Star Brawl 2", "Pocket Bravery", "Street Fighter 6"]},
    20: {"Categoria": "Melhor Jogo para Família - 3 pontos", "Opções": ["Disney Illusion Island", "Party Animals", "Pikmin 4", "Sonic Superstars", "Super Mario Bros. Wonder"]},
    21: {"Categoria": "Melhor Jogo de Simulação / Estratégia - 2 pontos", "Opções": ["Advance Wars 1+2: Re-boot camp", "Cities: Skylines II", "Company of Heroes 3", "Fire Emblem Engage", "Pikmin 4"]},
    22: {"Categoria": "Melhor Jogo de Esporte / Corrida - 2 pontos", "Opções": ["EA Sports FC 24", "F1 23", "Forza Motorspot", "Hot Wheels Unleashed 2: Turbocharged", "The Crew Motorfest"]},
    23: {"Categoria": "Melhor Jogo Multiplayer - 2 pontos", "Opções": ["Baldur's Gate 3", "Diablo IV", "Party Animals", "Street Fighter 6", "Super Mario Bros. Wonder"]},
    24: {"Categoria": "Melhor Adaptação - 2 pontos", "Opções": ["Castlevania: Nocturne", "Gran Turismo", "The Last of Us", "Super Mario Bros.: O Filme", "Twisted Metal"]},
    25: {"Categoria": "Jogo Mais Aguardado de 2024 - 2 pontos", "Opções": ["Final Fantasy VII Rebirth", "Hades II", "Like a Dragon: Infinite Wealth", "Star Wars Outlaws", "Tekken 8"]},
}


#DIA 7 DE DEZEMBRO CORRIGIR!
def respostas_ganhadores_df():
    return pd.DataFrame({
        "Jogo do Ano - 10 pontos": ['''Baldur's Gate 3'''],
        "Melhor Direção de Jogo - 5 pontos": ['''Alan Wake 2'''],
        "Melhor Narrativa - 5 pontos": ['''Alan Wake 2'''],
       "Melhor Direção de Arte - 5 pontos": ['''Alan Wake 2'''],
       "Melhor Trilha Sonora - 5 pontos": ['''Final Fantasy XVI, por Masayoshi Soken'''],
       "Melhor Design de Áudio - 5 pontos": ['''Hi-Fi Rush'''],
       "Melhor Atuação - 5 pontos": ['''"Neil Newbon, por Baldur's Gate 3"'''],
       "Inovação em Acessibilidade - 5 pontos": ['''Forza Motorsport'''],
       "Jogos com Maior Impacto Social - 5 pontos": ['''Tchia'''],
       "Melhor Jogo Contínuo - 5 pontos": ['''Cyberpunk 2077'''],
       "Melhor Suporte Comunitário - 3 pontos": ['''Baldur's Gate 3'''],
       "Melhor Jogo Independente - 3 pontos": ['''Sea of Stars'''],
       "Melhor Estreia de um Estúdio Indie - 3 pontos": ['''Coccoon'''],
       "Melhor Jogo Mobile - 3 pontos": ['''Honkai: Star Rail'''],
       "Melhor VR / AR - 3 pontos": ['''Resident Evil Village VR Mode'''],
       "Melhor Jogo de Ação - 3 pontos": ["""Armored Core VI: Fires of Rubicorn"""],
       "Melhor Jogo de Ação / Aventura - 3 pontos": ['''The Legend of Zelda: Tears of the Kingdom'''],
       "Melhor RPG - 3 pontos": ['''Baldur's Gate 3'''],
       "Melhor Jogo de Luta - 3 pontos": ['''Street Fighter 6'''],
       "Melhor Jogo para Família - 3 pontos": ['''Super Mario Bros. Wonder'''],
       "Melhor Jogo de Simulação / Estratégia - 2 pontos": ['''Pikmin 4'''],
       "Melhor Jogo de Esporte / Corrida - 2 pontos": ['''Forza Motorspot'''],
       "Melhor Jogo Multiplayer - 2 pontos": ['''Baldur's Gate 3'''],
       "Melhor Adaptação - 2 pontos": ['''The Last of Us'''],
       "Jogo Mais Aguardado de 2024 - 2 pontos": ['''Final Fantasy VII Rebirth''']
    })
