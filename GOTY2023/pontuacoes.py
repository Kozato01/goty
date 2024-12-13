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
        "Melhor Suporte à Comunidade - 3 pontos": 3,
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
        "Jogo Mais Aguardado de 2025 - 2 pontos": 2,
    }

    return pontuacao_por_categoria.get(categoria, 0)


def obter_categorias_escolhidas():
    return {
        1: {
            "Categoria": "Jogo do Ano - 10 pontos",
            "Opções": [
                "Elden Ring Shadow Of The Erdtree",
                "Black Myth: Wukong",
                "Astro Bot",
                "Balatro",
                "Final Fantasy 7 Rebirth",
                "Metaphor: ReFantazio",
            ],
        },
        2: {
            "Categoria": "Melhor Direção de Jogo - 5 pontos",
            "Opções": [
                "Astro Bot",
                "Balatro",
                "Elden Ring Shadow Of The Erdtree",
                "Final Fantasy 7 Rebirth",
                "Black Myth: Wukong",
                "Metaphor: ReFantazio",
            ],
        },
        3: {
            "Categoria": "Melhor Narrativa - 5 pontos",
            "Opções": [
                "Final Fantasy 7 Rebirth",
                "Like a Dragon Infinite Wealth",
                "Metaphor ReFantazio",
                "Senua’s Saga Hellblade 2",
                "Silent Hill 2",
            ],
        },
        4: {
            "Categoria": "Melhor Direção de Arte - 5 pontos",
            "Opções": [
                "Astro Bot",
                "Black Myth Wukong",
                "Elden Ring Shadow of the Erdtree",
                "Metaphor ReFantazio",
                "Neva",
            ],
        },
        5: {
            "Categoria": "Melhor Trilha Sonora - 5 pontos",
            "Opções": [
                "Astro Bot",
                "Final Fantasy 7 Rebirth",
                "Metaphor ReFantazio",
                "Silent Hill 2",
                "Stellar Blade",
            ],
        },
        6: {
            "Categoria": "Melhor Design de Áudio - 5 pontos",
            "Opções": [
                "Astro Bot",
                "Call of Duty Black Ops 6",
                "Final Fantasy 7 Rebirth",
                "Senua’s Saga Hellblade 2",
                "Silent Hill 2",
            ],
        },
        7: {
            "Categoria": "Melhor Atuação - 5 pontos",
            "Opções": [
                "Briana White (Aerith, de Final Fantasy 7 Rebirth)",
                "Hannah Telle (Max, de Life is Strange Double Exposure)",
                "Humberly Gonzáles (Kay Vess, de Star Wars Outlaws)",
                "Luke Roberts (James, de Silent Hill 2)",
                "Melina Juergens (Senua, de Hellblade 2)",
            ],
        },
        8: {
            "Categoria": "Inovação em Acessibilidade - 5 pontos",
            "Opções": [
                "Call of Duty Black Ops 6",
                "Diablo 4",
                "Dragon Age The Veilguard",
                "Prince of Persia The Lost Crown",
                "Star Wars Outlaws",
            ],
        },
        9: {
            "Categoria": "Jogos com Maior Impacto Social - 5 pontos",
            "Opções": [
                "Closer the Distance",
                "Indika",
                "Neva",
                "Life is Strange Double Exposure",
                "Senua’s Saga Hellblade 2",
                "Tales of Kenzera Zau",
            ],
        },
        10: {
            "Categoria": "Melhor Jogo Contínuo - 5 pontos",
            "Opções": [
                "Destiny 2",
                "Diablo 4",
                "Final Fantasy 14",
                "Fortnite",
                "Helldivers 2",
            ],
        },
        11: {
            "Categoria": "Melhor Suporte à Comunidade - 3 pontos",
            "Opções": [
                "Baldur’s Gate 3",
                "Final Fantasy 14",
                "Fortnite",
                "Helldivers 2",
                "No Man’s Sky",
            ],
        },
        12: {
            "Categoria": "Melhor Jogo Independente - 3 pontos",
            "Opções": [
                "Animal Well",
                "Balatro",
                "Lorelei and the Laser Eyes",
                "Neva",
                "UFO 50",
            ],
        },
        13: {
            "Categoria": "Melhor Estreia de um Estúdio Indie - 3 pontos",
            "Opções": [
                "Animal Well",
                "Balatro",
                "Manor Lords",
                "Pacific Drive",
                "The Plucky Squire",
            ],
        },
        14: {
            "Categoria": "Melhor Jogo Mobile - 3 pontos",
            "Opções": [
                "AFK Journey",
                "Balatro",
                "Pokémon TCG Pocket",
                "Wuthering Waves",
                "Zenless Zone Zero",
            ],
        },
        15: {
            "Categoria": "Melhor VR / AR - 3 pontos",
            "Opções": [
                "Arizona Sunshine Remake",
                "Asgard’s Wrath 2",
                "Batman Arkham Shadow",
                "Metal Hellsinger VR",
                "Metro Awakening",
            ],
        },
        16: {
            "Categoria": "Melhor Jogo de Ação - 3 pontos",
            "Opções": [
                "Black Myth Wukong",
                "Call of Duty Black Ops 6",
                "Helldivers 2",
                "Warhammer 40K Space Marine 2",
                "Stellar Blade",
            ],
        },
        17: {
            "Categoria": "Melhor Jogo de Ação / Aventura - 3 pontos",
            "Opções": [
                "Astro Bot",
                "Prince of Persia The Lost Crown",
                "Silent Hill 2",
                "Star Wars Outlaws",
                "Zelda Echoes of Wisdom",
            ],
        },
        18: {
            "Categoria": "Melhor RPG - 3 pontos",
            "Opções": [
                "Dragon’s Dogma 2",
                "Elden Ring Shadow of the Erdtree",
                "Final Fantasy 7 Rebirth",
                "Like a Dragon Infinite Wealth",
                "Metaphor ReFantazio",
            ],
        },
        19: {
            "Categoria": "Melhor Jogo de Luta - 3 pontos",
            "Opções": [
                "Dragon Ball Sparking Zero",
                "Granblue Fantasy Versus Rising",
                "Marvel vs. Capcom Fighting Collection Arcade Classics",
                "Multiversus",
                "Tekken 8",
            ],
        },
        20: {
            "Categoria": "Melhor Jogo para Família - 3 pontos",
            "Opções": [
                "Astro Bot",
                "Princess Peach Showtime",
                "Super Mario Party Jamboree",
                "The Legend of Zelda Echoes of Wisdom",
                "The Plucky Squire",
            ],
        },
        21: {
            "Categoria": "Melhor Jogo de Simulação / Estratégia - 2 pontos",
            "Opções": [
                "Age of Mythology Retold",
                "Frostpunk 2",
                "Kunitsu-Gami Path of the Goddess",
                "Manor Lords",
                "Unicorn Overlord",
            ],
        },
        22: {
            "Categoria": "Melhor Jogo de Esporte / Corrida - 2 pontos",
            "Opções": [
                "F1 24",
                "EA Sports FC 25",
                "NBA 2K25",
                "Top Spin 2K25",
                "WWE 2K24",
            ],
        },
        23: {
            "Categoria": "Melhor Jogo Multiplayer - 2 pontos",
            "Opções": [
                "Call of Duty Black Ops 6",
                "Helldivers 2",
                "Mario Party Jamboree",
                "Tekken 8",
                "Warhammer 40K Space Marine 2",
            ],
        },
        24: {
            "Categoria": "Melhor Adaptação - 2 pontos",
            "Opções": [
                "Arcane",
                "Fallout",
                "Knuckles",
                "Like a Dragon Yakuza",
                "Tomb Raider The Legend of Lara Croft",
            ],
        },
        25: {
            "Categoria": "Jogo Mais Aguardado de 2025 - 2 pontos",
            "Opções": [
                "Death Stranding 2 On the Beach",
                "Ghost of Yotei",
                "GTA 6",
                "Metroid Prime 4 Beyond",
                "Monster Hunter Wilds",
            ],
        },
    }


# DIA 7 DE DEZEMBRO CORRIGIR!
def respostas_ganhadores_df():
    return pd.DataFrame(
        {
            "Jogo do Ano - 10 pontos": [""""""],
            "Melhor Direção de Jogo - 5 pontos": ["""Astro Bot"""],
            "Melhor Narrativa - 5 pontos": ["""Metaphor ReFantazio"""],
            "Melhor Direção de Arte - 5 pontos": ["""Metaphor ReFantazio"""],
            "Melhor Trilha Sonora - 5 pontos": ["""Final Fantasy 7 Rebirth"""],
            "Melhor Design de Áudio - 5 pontos": ["""Senua’s Saga Hellblade 2"""],
            "Melhor Atuação - 5 pontos": ["""Melina Juergens (Senua, de Hellblade 2)"""],
            "Inovação em Acessibilidade - 5 pontos": ["""Prince of Persia The Lost Crown"""],
            "Jogos com Maior Impacto Social - 5 pontos": ["""Neva"""],
            "Melhor Jogo Contínuo - 5 pontos": ["""Helldivers 2"""],
            "Melhor Suporte à Comunidade - 3 pontos": ["""Baldur’s Gate 3"""],
            "Melhor Jogo Independente - 3 pontos": ["""Balatro"""],
            "Melhor Estreia de um Estúdio Indie - 3 pontos": ["""Balatro"""],
            "Melhor Jogo Mobile - 3 pontos": ["""Balatro"""],
            "Melhor VR / AR - 3 pontos": ["""Batman Arkham Shadow"""],
            "Melhor Jogo de Ação - 3 pontos": ["""Black Myth Wukong"""],
            "Melhor Jogo de Ação / Aventura - 3 pontos": ["""Astro Bot"""],
            "Melhor RPG - 3 pontos": ["""Metaphor ReFantazio"""],
            "Melhor Jogo de Luta - 3 pontos": ["""Tekken 8"""],
            "Melhor Jogo para Família - 3 pontos": ["""Astro Bot"""],
            "Melhor Jogo de Simulação / Estratégia - 2 pontos": ["""Frostpunk 2"""],
            "Melhor Jogo de Esporte / Corrida - 2 pontos": ["""EA Sports FC 25"""],
            "Melhor Jogo Multiplayer - 2 pontos": ["""Helldivers 2"""],
            "Melhor Adaptação - 2 pontos": ["""Fallout"""],
            "Jogo Mais Aguardado de 2025 - 2 pontos": ["""GTA 6"""],
        }
    )
