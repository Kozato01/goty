import pandas as pd
import requests
import streamlit as st
import base64
import git
from io import StringIO
from pontuacoes import obter_pontos_por_categoria


#DIA 7 DE DEZEMBRO CORRIGIR!
def Resultado():
    return pd.DataFrame({
    #  "Jogo do Ano - 10 pontos": [],
    #   "Melhor Direção de Jogo - 5 pontos": [],
    #   "Melhor Narrativa - 5 pontos": [],
    #   "Melhor Direção de Arte - 5 pontos": [],
    #   "Melhor Trilha Sonora - 5 pontos": [],
    #   "Melhor Design de Áudio - 5 pontos": [],
    #   "Melhor Atuação - 5 pontos": [],
    #   "Inovação em Acessibilidade - 5 pontos": [],
    #   "Jogos com Maior Impacto Social - 5 pontos": [],
    #   "Melhor Jogo Contínuo - 5 pontos": [],
    #   "Melhor Suporte Comunitário - 3 pontos": [],
    #   "Melhor Jogo Independente - 3 pontos": [],
    #   "Melhor Estreia de um Estúdio Indie - 3 pontos": [],
    #   "Melhor Jogo Mobile - 3 pontos": [],
    #   "Melhor VR / AR - 3 pontos": [],
    #   "Melhor Jogo de Ação - 3 pontos": [],
    #   "Melhor Jogo de Ação / Aventura - 3 pontos": [],
    #   "Melhor RPG - 3 pontos": [],
    #   "Melhor Jogo de Luta - 3 pontos": [],
    #   "Melhor Jogo para Família - 3 pontos": [],
    #   "Melhor Jogo de Simulação / Estratégia - 2 pontos": [],
    #   "Melhor Jogo de Esporte / Corrida - 2 pontos": [],
    #   "Melhor Jogo Multiplayer - 2 pontos": [],
    #   "Melhor Adaptação - 2 pontos": [],
    #   "Jogo Mais Aguardado de 2024 - 2 pontos": []
    })

def exibir_escolhas_usuario(categorias_escolhidas):
    # Exibir escolhas do usuário em uma tabela
    escolhas_usuario_df = pd.DataFrame(categorias_escolhidas.items(), columns=["Categoria", "Escolha"]).set_index("Categoria").T
    st.table(escolhas_usuario_df)

def carregar_respostas():
    github_raw_url = "https://github.com/Kozato01/goty/blob/main/GOTY2023/respostas.csv"

    try:
        # Baixar o conteúdo do arquivo CSV do GitHub
        response = requests.get(github_raw_url)
        response.raise_for_status()  # Verificar se houve algum erro no download

        # Ler o conteúdo do CSV a partir do texto retornado pela requisição
        csv_content = StringIO(response.text)

        # Tentar carregar respostas do arquivo CSV
        return pd.read_csv(csv_content)
    
    except requests.exceptions.RequestException as e:
        # Lidar com erros de requisição
        print(f"Erro ao baixar o arquivo CSV do GitHub: {e}")
        return pd.DataFrame()
    
    except pd.errors.EmptyDataError:
        # Se o arquivo estiver vazio, retornar DataFrame vazio
        return pd.DataFrame()

def usuario_existente(respostas_df, email, nome, telegram):
    # Verificar se o usuário já existe no DataFrame
    if not respostas_df.empty and "Email" in respostas_df.columns and "Nome" in respostas_df.columns and "Nome no Telegram" in respostas_df.columns:
        usuario_existente = (
            (respostas_df["Email"] == email) |
            (respostas_df["Nome"] == nome) |
            (respostas_df["Nome no Telegram"] == telegram)
        )
        return usuario_existente.any()
    else:
        return False
    


def download_csv_link(df, filename="resultado_usuario.csv"):
    csv = df.to_csv(index=False, encoding="utf-8")
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Baixar Resultado</a>'
    return href

def visualizar_respostas(email, nome, respostas_ganhadores_df=None):
    respostas_df = carregar_respostas()
    usuario_df = respostas_df[(respostas_df["Email"] == email) & (respostas_df["Nome"] == nome)]

    if usuario_df.empty:
        st.warning("Nenhuma resposta encontrada para o usuário.")
    else:
        # Exibir respostas do usuário em uma tabela
        st.markdown(
            f"<h2 style='color: #ff6600; margin-top: 30px; background: linear-gradient(to right, #333333, #666666); padding: 10px; border-radius: 5px;'>Respostas de {nome}</h2>",
            unsafe_allow_html=True,
        )
        st.table(usuario_df.style.set_table_styles([{"selector": "th", "props": [("background-color", "#333333"), ("color", "#ff6600")]}]))

        # Adicionar botão para baixar o resultado em CSV
        st.markdown("<h3>Baixar Resultado</h3>", unsafe_allow_html=True)
        st.write("Clique no botão abaixo para baixar o resultado em CSV.")
        
        # Usar a função de download_csv_link para obter o link de download
        st.markdown(download_csv_link(usuario_df), unsafe_allow_html=True)

        # Contar pontos apenas se os ganhadores estiverem disponíveis
        if respostas_ganhadores_df is not None:
            pontos = contar_pontos(usuario_df, respostas_ganhadores_df)
            st.success(f"Você acumulou {pontos} pontos com suas respostas.")


def contar_pontos(usuario_df, respostas_ganhadores_df):
    pontos = 0

    # Iterar sobre as colunas de respostas do usuário
    for categoria, escolha_usuario in usuario_df.items():
        if categoria in respostas_ganhadores_df.columns:
            # Verificar se a escolha do usuário coincide com a escolha do ganhador
            escolha_ganhador = respostas_ganhadores_df[categoria].iloc[0]
            if escolha_usuario.iloc[0] == escolha_ganhador:
                # Adicionar pontos com base na categoria
                pontos += obter_pontos_por_categoria(categoria)

    return pontos


def exibir_formulario():
    # Criar campos de entrada para email, nome e nome no Telegram
    col1, col2, col3 = st.columns(3)
    with col1:
        email = st.text_input("Email:").lower()
    with col2:
        nome = st.text_input("Nome:").lower()
    with col3:
        telegram = st.text_input("Nome no Telegram:").lower()

    # Verificar se os campos de nome, email e telegram foram preenchidos corretamente
    if not email or not "@" in email:
        st.warning("Por favor, insira um endereço de e-mail válido.")
        return

    if not nome:
        st.warning("Por favor, insira seu nome.")
        return

    if not telegram:
        st.warning("Por favor, insira seu nome no Telegram.")
        return

    # Dicionário de categorias e opções
    categorias_opcoes = {
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


    # Inicializar categorias escolhidas
    categorias_escolhidas = {}

    # Carregar respostas existentes do arquivo CSV
    respostas_df = carregar_respostas()

    # Verificar se o usuário já preencheu o formulário
    if usuario_existente(respostas_df, email, nome, telegram):
        st.warning("Você já preencheu o formulário. Não é permitido preencher novamente.")
        return


    # Loop para coletar respostas do usuário
    for numero, info_categoria in categorias_opcoes.items():
        categoria = info_categoria["Categoria"]
        opcoes = info_categoria["Opções"]

        if st.checkbox(f"{numero}. Escolher {categoria}", key=categoria):
            # Mensagem informativa antes da caixa de seleção
            st.write("Clique abaixo para ver as opções:")
            with st.expander(f"Opções para {categoria}", expanded=False):
                opcao_escolhida = st.selectbox(f"Escolha a opção em {categoria}:", opcoes)
                categorias_escolhidas[categoria] = opcao_escolhida

            # Adicionando ícone de confirmação à direita do expander
            st.markdown('<div style="float: right; margin-right: 20px;"><span style="color:green">&#10004;</span> Categoria escolhida: {}</div>'.format(categoria), unsafe_allow_html=True)

    # Estilizando a tabela de escolhas do usuário
    st.markdown(
        "<h2 style='color: #ff6600; margin-top: 30px; background: linear-gradient(to right, #333333, #666666); padding: 10px; border-radius: 5px;'>Suas Escolhas</h2>",
        unsafe_allow_html=True,
    )
    escolhas_usuario_df = pd.DataFrame(categorias_escolhidas.items(), columns=["Categoria", "Escolha"]).set_index("Categoria").T
    st.table(escolhas_usuario_df.style.set_table_styles([{"selector": "th", "props": [("background-color", "#333333"), ("color", "#ff6600")]}]))

    # Adicionar campos de email, nome e nome no Telegram ao dicionário
    categorias_escolhidas["Email"] = email
    categorias_escolhidas["Nome"] = nome
    categorias_escolhidas["Nome no Telegram"] = telegram

    # Botão de confirmação
    if st.button("Confirmar e Salvar Respostas"):
        novas_respostas_df = pd.DataFrame(categorias_escolhidas, index=[0])
        respostas_df = pd.concat([respostas_df, novas_respostas_df], ignore_index=True)

        # Salvar respostas localmente
        respostas_df.to_csv("respostas.csv", index=False)
        st.success("Respostas salvas localmente com sucesso!")

        # Salvar no GitHub
        try:
            repo = git.Repo("caminho/para/seu/repositorio")  # Substitua com o caminho do seu repositório
            repo.git.add("respostas.csv")
            repo.git.commit(m="Atualizando respostas")
            repo.git.push()
            st.success("Respostas salvas no GitHub com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar no GitHub: {str(e)}")

def baixar_respostas_usuario(email, nome):
    respostas_df = carregar_respostas()
    usuario_df = respostas_df[(respostas_df["Email"] == email) & (respostas_df["Nome"] == nome)]
    if not usuario_df.empty:
        respostas_usuario_df = pd.concat([Resultado(), usuario_df], ignore_index=True)
        caminho_csv_usuario = f"{nome}_respostas.csv"
        respostas_usuario_df.to_csv(caminho_csv_usuario, index=False)
        st.success(f"**Respostas de {nome} salvas em {caminho_csv_usuario}.**")
        #st.markdown(f"**[Baixar suas respostas](sandbox:/view/{caminho_csv_usuario})**")

    else:
        st.warning("Nenhuma resposta encontrada para o usuário.")
