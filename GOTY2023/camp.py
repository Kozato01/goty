import pandas as pd
import streamlit as st
import re
import os
import snowflake.connector
from snowflake.connector import ProgrammingError
from pontuacoes import (
    obter_categorias_escolhidas,
    obter_pontos_por_categoria,
    respostas_ganhadores_df,
)
from datetime import datetime
import warnings
from dotenv import load_dotenv

load_dotenv()


warnings.simplefilter(action="ignore", category=FutureWarning)

# Constantes
TABELA_PADRAO = "GOTY2024"
cursor = None


# Funciona o deleta do usuario.
def apagar_dados_usuario(connection, tabela, email, nome, telegram):
    cursor = None  # Definir cursor antes do bloco try
    try:
        cursor = connection.cursor()
        # Verificar se a tabela existe
        if not tabela_existe(cursor, tabela):
            st.warning(f"A tabela '{tabela}' não existe.")
            return

        data_limite_exclusao = datetime(2024, 12, 7)
        data_atual = datetime.now()

        if data_atual > data_limite_exclusao:
            st.warning("Não é permitido excluir dados após 07/12/2024.")
            return
        if not verificar_existencia_usuario(connection, email, nome, telegram, tabela):
            st.warning("Usuário não encontrado. Nenhum dado foi excluído.")
            return
        query = f"DELETE FROM {tabela} WHERE Email = %s AND Nome = %s AND Telegram = %s"
        cursor.execute(query, (email, nome, telegram))
        connection.commit()

        st.success("Dados do usuário excluídos com sucesso!")

    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao excluir dados do usuário: {str(e)}")

    except Exception as ex:
        st.error(f"Ocorreu um erro inesperado ao excluir dados do usuário: {str(ex)}")
    finally:
        if cursor is not None:
            fechar_cursor(cursor)


# Formulario de exclusão
def exibir_formulario_exclusao():
    # Adicionar estilo ao título
    st.markdown(
        """
        <div style='background: linear-gradient(to right, #16202c, #394e6c); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: #fcfdfd; text-align: center; font-weight: bold;'>
                <img src='https://medlimp.com.br/wp-content/uploads/2023/03/LIXEIRA-BRANCA-50L-SEM-POSTE-COM-HASTE-METALICA-JSN.png' 
                style='vertical-align: middle; height: 1em;'/> Excluir Dados do Usuário
            </h1>
            <p style='color: #394e6c; font-size: 16px; text-align: center; background: #fcfdfd; padding: 15px; border-radius: 8px; font-weight: bold;'>
                🚨 <strong>IMPORTANTE:</strong> A exclusão de dados é uma ação <strong>definitiva</strong> e <strong>irreversível</strong>. 
                Utilize esta opção apenas para corrigir informações ou refazer o formulário.
                Após a exclusão, <strong>não será possível recuperar os dados</strong>. Verifique com cuidado antes de confirmar esta ação.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        email_exclusao = st.text_input("Email:").lower()
    with col2:
        nome_exclusao = st.text_input("Nome:").lower()
    with col3:
        telegram_exclusao = st.text_input("Nome no Telegram:").lower()

    if st.button("Excluir Meus Dados"):
        apagar_dados_usuario(
            connection, "GOTY2024", email_exclusao, nome_exclusao, telegram_exclusao
        )


# Funções de Conexão
def conectar_snowflake(account, username, password, warehouse, database, schema=None):
    try:
        connection = snowflake.connector.connect(
            user=username,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema,
        )
        return connection
    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao conectar ao Snowflake: {str(e)}")
        return None


# Funções de Verificação
def verificar_existencia_usuario(
    connection, email=None, nome=None, telegram=None, tabela=TABELA_PADRAO
):
    cursor = None  # Inicializa cursor fora do bloco try
    try:
        cursor = connection.cursor()
        if not tabela_existe(cursor, tabela):
            # st.warning(f"A tabela '{tabela}' não existe.")
            return False

        if email and nome and telegram:
            # Consulta com todos os parâmetros
            query = f"SELECT * FROM {tabela} WHERE Email = %s AND Nome = %s AND Telegram = %s"
            cursor.execute(query, (email, nome, telegram))
        elif email and telegram:
            # Consulta com email e nome
            query = f"SELECT * FROM {tabela} WHERE Email = %s AND Telegram = %s"
            cursor.execute(query, (email, telegram))
        else:
            st.warning("Usuario não encontrando ou não existe.")
            return False

        return cursor.fetchone() is not None
    except snowflake.connector.errors.ProgrammingError as e:
        st.error(f"Erro ao executar consulta: {str(e)}")
        return False
    except Exception as ex:
        st.error(f"Ocorreu um erro inesperado: {str(ex)}")
        return False
    finally:
        fechar_cursor(cursor)


# Funções de Tabela
def tabela_existe(cursor, tabela):
    cursor.execute(f"SHOW TABLES LIKE '{tabela.upper()}'")
    return bool(cursor.fetchone())


# Função de inserir dados no banco, funciona.
def inserir_dados_usuario(connection, tabela, email, nome, telegram, respostas_usuario):
    cursor = None
    try:
        cursor = connection.cursor()
        if verificar_existencia_usuario(connection, email, nome, telegram, tabela):
            st.warning(
                "⚠️ Você já preencheu o formulário. Não é permitido preencher novamente. Você pode apagar sua aposta atual até o dia 02/11/2024, caso queira preencher de novo."
            )
            return
        colunas_categorias = [
            re.sub(r"[^a-zA-Z0-9_]", "_", categoria.split("-")[0].strip())
            for categoria in respostas_usuario.keys()
        ]
        colunas_query = ", ".join(colunas_categorias)
        placeholders = ", ".join(["%s" for _ in respostas_usuario.values()])
        query = f"INSERT INTO {tabela} (email, nome, telegram, {colunas_query}) VALUES (%s, %s, %s, {placeholders})"
        valores_insercao = [email, nome, telegram, *respostas_usuario.values()]
        cursor.execute(query, valores_insercao)
        connection.commit()
        st.success("✨ Suas respostas para o GOTY foram cadastradas! Boa sorte! 🏆")
    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao inserir dados do usuário: {str(e)}")
    except Exception as ex:
        st.error(f"Ocorreu um erro inesperado ao inserir dados do usuário: {str(ex)}")
    finally:
        fechar_cursor(cursor)


# função pra criar tabela sql no snow
def criar_tabela_sql(connection, tabela, categorias_escolhidas):
    cursor = None  # Inicializa cursor fora do bloco try
    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{tabela.upper()}'")
        tabela_existe = bool(cursor.fetchone())
        if not tabela_existe:
            colunas_categorias = [
                re.sub(
                    r"[^a-zA-Z0-9_]",
                    "_",
                    categoria_info["Categoria"].split("-")[0].strip(),
                )
                for categoria_info in categorias_escolhidas.values()
            ]

            query = f"""
                CREATE TABLE IF NOT EXISTS public.{tabela} (
                    email STRING,
                    nome STRING,
                    telegram STRING,
                    {' STRING, '.join(colunas_categorias)} STRING
                );
            """
            cursor.execute(query)
            connection.commit()
            # st.success(f"Tabela '{tabela}' criada com sucesso!")
    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao criar tabela: {str(e)}")
    except Exception as ex:
        st.error(f"Ocorreu um erro inesperado ao criar tabela: {str(ex)}")
    finally:
        fechar_cursor(cursor)


# Funções de Interface do formulario
def exibir_formulario():
    st.markdown(
        """
        <h1 style="color: #fcfdfd; margin-top: 20px; background: linear-gradient(to right, #16202c, #394e6c); padding: 15px; border-radius: 8px; text-align: center; font-weight: bold;">
        <img src="https://cdn.worldvectorlogo.com/logos/the-game-awards.svg" style="vertical-align: middle; height: 1em;" /> Votação - The Game Awards
    </h1>
    <div style="background: linear-gradient(to right, #16202c, #394e6c); padding: 20px; border-radius: 10px;">
        <p style="color: #394e6c; font-size: 16px; text-align: center; background: #fcfdfd; padding: 15px; border-radius: 4px;">
            🎮 Bem-vindo ao Formulário de Votação do The Game Awards! Este é um evento descontraído entre amigos.
            Os resultados serão anunciados em 7 de Dezembro de 2024. Boa sorte!
            Para discussões e mais informações, participe do nosso grupo no 
            <a href="https://t.me/monsterhunterbr" target="_blank" style="color: #394e6c;">
                <img src="https://img.icons8.com/color/24/000000/telegram-app--v5.png" alt="Telegram" />
                Grupo do Telegram
            </a>.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        email = st.text_input("Email:").lower()
    with col2:
        nome = st.text_input("Nome:").lower()
    with col3:
        telegram = st.text_input("Nome no Telegram:").lower()

    if not email or not "@" in email:
        st.warning("Por favor, insira um endereço de e-mail válido.")
        return

    if not nome:
        st.warning("Por favor, insira seu nome.")
        return

    if not telegram:
        st.warning("Por favor, insira seu nome no Telegram.")
        return
    categorias_escolhidas = obter_categorias_escolhidas()
    if verificar_existencia_usuario(connection, email, nome, telegram):
        st.warning(
            "Você já preencheu o formulário. Não é permitido preencher novamente."
        )
        return

    respostas_usuario = obter_respostas_usuario(categorias_escolhidas)
    exibir_escolhas_usuario(respostas_usuario)
    if st.button("Confirmar e Salvar Respostas"):
        criar_tabela_sql(connection, "GOTY2024", categorias_escolhidas)
        inserir_dados_usuario(
            connection, "GOTY2024", email, nome, telegram, respostas_usuario
        )


# Funções Auxiliares
def obter_respostas_usuario(categorias_escolhidas):
    respostas_usuario = {}

    for numero, categoria_info in categorias_escolhidas.items():
        categoria = categoria_info["Categoria"]
        opcoes = categoria_info["Opções"]
        if st.checkbox(
            f"**{numero}. Escolher {categoria}**", key=categoria, value=False
        ):
            opcao_escolhida = st.selectbox(
                "Escolha uma opção:",
                [""] + opcoes,
                index=0,
            )

            respostas_usuario[categoria] = opcao_escolhida
            categoria_nome = categoria.split(" -")[0]

            st.markdown(
                f"""
                <div style="float: right; margin-right: 20px; 
                            color: #ffffff; 
                            background: linear-gradient(to right, #394e6c, #16202c); 
                            font-weight: bold; 
                            padding: 8px 15px; 
                            border-radius: 12px; 
                            font-size: 16px; 
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); 
                            text-transform: uppercase; 
                            letter-spacing: 1px; 
                            transition: transform 0.3s ease;">
                    &#10004; Categoria: <span style="color: #b0c4de; font-weight: normal;">{categoria}</span> 
                    <br>
                    Sua Escolha: <span style="color: #32CD32; font-weight: normal; font-size: 18px; font-style: italic;">{respostas_usuario.get(categoria, "Não informado")}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    escolhas_usuario_df = pd.DataFrame.from_dict(
        respostas_usuario, orient="index", columns=["Escolha"]
    )

    return respostas_usuario


def exibir_escolhas_usuario(categorias_escolhidas):
    st.markdown(
        """
    <h2 style='color: #ffffff; margin-top: 20px; background: linear-gradient(to right, #394e6c, #16202c); padding: 15px; border-radius: 8px; text-align: center; font-weight: bold;'>Respostas Cadastradas</h2>
    """,
        unsafe_allow_html=True,
    )

    # Criando o DataFrame a partir dos dados fornecidos
    escolhas_usuario_df = pd.DataFrame.from_dict(
        categorias_escolhidas, orient="index", columns=["Escolha"]
    )

    # Substituindo valores vazios ou espaços em branco por "Não Escolhido"
    escolhas_usuario_df["Escolha"] = escolhas_usuario_df["Escolha"].apply(
        lambda x: "Não Escolhido" if not x or x.strip() == "" else x
    )

    # Resetando o índice para que a coluna de categorias apareça como uma coluna regular
    escolhas_usuario_df.reset_index(inplace=True)

    # Renomeando as colunas para "Categoria" e "Escolha"
    escolhas_usuario_df.columns = ["Categoria", "Escolha"]

    # Convertendo o DataFrame para HTML com classes
    html_table = escolhas_usuario_df.to_html(
        classes="dataframe", index=False, escape=False
    )

    # CSS para estilizar a tabela
    css = """
    <style>
        .dataframe {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;  /* Tamanho de fonte reduzido */
            color: #ffffff;
            background-color: #16202c;
            border-radius: 10px;
        }
        .dataframe th, .dataframe td {
            padding: 15px;  /* Menor padding para uma tabela mais compacta */
            text-align: center;
            border: 1px solid #394e6c;
        }
        .dataframe th {
            background: linear-gradient(to right, #394e6c, #16202c);
            color: #ffffff;
            font-weight: bold;
        }
        .dataframe tr:nth-child(even) {
            background: #1e2a3a;
        }
        .dataframe tr:hover {
            background-color: #444444;
        }
        .dataframe td {
            color: #ffffff;
        }
        .dataframe td:hover {
            background-color: #444444;
            cursor: pointer;
        }
        .dataframe tr:first-child th {
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        .dataframe tr:last-child td {
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }
    </style>
    """

    # Exibindo a tabela estilizada no Streamlit
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)


def exibir_formulario_visualizacao_respostas():
    st.markdown(
        """
        <div style='background: linear-gradient(to right, #16202c, #394e6c); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: #fcfdfd; text-align: center; font-weight: bold;'>
                <img src='https://cdn3.iconfinder.com/data/icons/web-and-seo-31/16/invisible-eye-512.png' 
                style='vertical-align: middle; height: 1em;'/> Visualizar Respostas
            </h1>
            <p style='color: #394e6c; font-size: 16px; text-align: center; background: #fcfdfd; padding: 15px; border-radius: 8px;'>
                📋 Aqui você pode visualizar suas respostas cadastradas no formulário. No dia do evento, você saberá quantos pontos acumulou com suas escolhas!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email:").lower()
    with col2:
        telegram = st.text_input("Nome no Telegram:").lower()

    if st.button("Visualizar Respostas"):
        visualizar_respostas_usuario(email, telegram, connection, "GOTY2024")

    if st.sidebar.button("Participantes"):
        usuariosescolhas(connection, "usuariosgoty")


def usuariosescolhas(connection, tabela):
    try:
        cursor = connection.cursor()

        # Consultar todas as respostas dos usuários
        query = f"SELECT * FROM {tabela}"
        cursor.execute(query)
        usuarios_respostas = cursor.fetchall()

        # Criar DataFrame com as respostas dos usuários
        colunas = [desc[0] for desc in cursor.description]
        df_usuarios_respostas = pd.DataFrame(usuarios_respostas, columns=colunas)

        # Mapear as colunas para os novos nomes
        novo_nome_colunas = {
            "JOGO_DO_ANO": "Jogo do Ano - 10 pontos",
            "MELHOR_DIRE__O_DE_JOGO": "Melhor Direção de Jogo - 5 pontos",
            "MELHOR_NARRATIVA": "Melhor Narrativa - 5 pontos",
            "MELHOR_DIRE__O_DE_ARTE": "Melhor Direção de Arte - 5 pontos",
            "MELHOR_TRILHA_SONORA": "Melhor Trilha Sonora - 5 pontos",
            "MELHOR_DESIGN_DE__UDIO": "Melhor Design de Áudio - 5 pontos",
            "MELHOR_ATUA__O": "Melhor Atuação - 5 pontos",
            "INOVA__O_EM_ACESSIBILIDADE": "Inovação em Acessibilidade - 5 pontos",
            "JOGOS_COM_MAIOR_IMPACTO_SOCIAL": "Jogos com Maior Impacto Social - 5 pontos",
            "MELHOR_JOGO_CONT_NUO": "Melhor Jogo Contínuo - 5 pontos",
            "MELHOR_SUPORTE___COMUNIDADE": "Melhor Suporte à Comunidade - 3 pontos",
            "MELHOR_JOGO_INDEPENDENTE": "Melhor Jogo Independente - 3 pontos",
            "MELHOR_ESTREIA_DE_UM_EST_DIO_INDIE": "Melhor Estreia de um Estúdio Indie - 3 pontos",
            "MELHOR_JOGO_MOBILE": "Melhor Jogo Mobile - 3 pontos",
            "MELHOR_VR___AR": "Melhor VR / AR - 3 pontos",
            "MELHOR_JOGO_DE_A__O": "Melhor Jogo de Ação - 3 pontos",
            "MELHOR_JOGO_DE_A__O___AVENTURA": "Melhor Jogo de Ação / Aventura - 3 pontos",
            "MELHOR_RPG": "Melhor RPG - 3 pontos",
            "MELHOR_JOGO_DE_LUTA": "Melhor Jogo de Luta - 3 pontos",
            "MELHOR_JOGO_PARA_FAM_LIA": "Melhor Jogo para Família - 3 pontos",
            "MELHOR_JOGO_DE_SIMULA__O___ESTRAT_GIA": "Melhor Jogo de Simulação / Estratégia - 2 pontos",
            "MELHOR_JOGO_DE_ESPORTE___CORRIDA": "Melhor Jogo de Esporte / Corrida - 2 pontos",
            "MELHOR_JOGO_MULTIPLAYER": "Melhor Jogo Multiplayer - 2 pontos",
            "MELHOR_ADAPTA__O": "Melhor Adaptação - 2 pontos",
            "JOGO_MAIS_AGUARDADO_DE_2025": "Jogo Mais Aguardado de 2025 - 2 pontos",
        }

        # Renomear as colunas
        df_usuarios_respostas = df_usuarios_respostas.rename(columns=novo_nome_colunas)

        # Exibir a tabela de respostas dos usuários
        st.dataframe(
            df_usuarios_respostas.style.set_table_styles(
                [
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", "#333333"),
                            ("color", "#ff6600"),
                        ],
                    }
                ]
            ).apply(
                lambda x: [
                    "background: linear-gradient(to right, #333333, #666666); color: #ff6600"
                ]
                * len(x),
                axis=1,
            )
        )

    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao consultar respostas dos usuários: {str(e)}")

    except Exception as ex:
        st.error(
            f"Ocorreu um erro inesperado ao consultar respostas dos usuários: {str(ex)}"
        )

    finally:
        fechar_cursor(cursor)


# Função para visualizar as respostas do usuário
def visualizar_respostas_usuario(email, telegram, connection, tabela):
    try:
        cursor = connection.cursor()

        # Verificar se a tabela existe
        if not tabela_existe(cursor, tabela):
            st.warning(f"A tabela '{tabela}' não existe.")
            return

        # Verificar se o usuário existe
        if not verificar_existencia_usuario(
            connection, email, telegram=telegram, tabela=tabela
        ):
            st.warning("Usuário não encontrado.")
            return

        # Consultar as respostas do usuário
        query = f"SELECT * FROM {tabela} WHERE Email = %s AND Telegram = %s"
        cursor.execute(query, (email, telegram))
        usuario_respostas = cursor.fetchone()

        # Criar um DataFrame com as respostas do usuário
        respostas_df = pd.DataFrame(
            [usuario_respostas], columns=[desc[0] for desc in cursor.description]
        )

        # Mapear as colunas para os novos nomes
        novo_nome_colunas = {
            "JOGO_DO_ANO": "Jogo do Ano - 10 pontos",
            "MELHOR_DIRE__O_DE_JOGO": "Melhor Direção de Jogo - 5 pontos",
            "MELHOR_NARRATIVA": "Melhor Narrativa - 5 pontos",
            "MELHOR_DIRE__O_DE_ARTE": "Melhor Direção de Arte - 5 pontos",
            "MELHOR_TRILHA_SONORA": "Melhor Trilha Sonora - 5 pontos",
            "MELHOR_DESIGN_DE__UDIO": "Melhor Design de Áudio - 5 pontos",
            "MELHOR_ATUA__O": "Melhor Atuação - 5 pontos",
            "INOVA__O_EM_ACESSIBILIDADE": "Inovação em Acessibilidade - 5 pontos",
            "JOGOS_COM_MAIOR_IMPACTO_SOCIAL": "Jogos com Maior Impacto Social - 5 pontos",
            "MELHOR_JOGO_CONT_NUO": "Melhor Jogo Contínuo - 5 pontos",
            "MELHOR_SUPORTE___COMUNIDADE": "Melhor Suporte à Comunidade - 3 pontos",
            "MELHOR_JOGO_INDEPENDENTE": "Melhor Jogo Independente - 3 pontos",
            "MELHOR_ESTREIA_DE_UM_EST_DIO_INDIE": "Melhor Estreia de um Estúdio Indie - 3 pontos",
            "MELHOR_JOGO_MOBILE": "Melhor Jogo Mobile - 3 pontos",
            "MELHOR_VR___AR": "Melhor VR / AR - 3 pontos",
            "MELHOR_JOGO_DE_A__O": "Melhor Jogo de Ação - 3 pontos",
            "MELHOR_JOGO_DE_A__O___AVENTURA": "Melhor Jogo de Ação / Aventura - 3 pontos",
            "MELHOR_RPG": "Melhor RPG - 3 pontos",
            "MELHOR_JOGO_DE_LUTA": "Melhor Jogo de Luta - 3 pontos",
            "MELHOR_JOGO_PARA_FAM_LIA": "Melhor Jogo para Família - 3 pontos",
            "MELHOR_JOGO_DE_SIMULA__O___ESTRAT_GIA": "Melhor Jogo de Simulação / Estratégia - 2 pontos",
            "MELHOR_JOGO_DE_ESPORTE___CORRIDA": "Melhor Jogo de Esporte / Corrida - 2 pontos",
            "MELHOR_JOGO_MULTIPLAYER": "Melhor Jogo Multiplayer - 2 pontos",
            "MELHOR_ADAPTA__O": "Melhor Adaptação - 2 pontos",
            "JOGO_MAIS_AGUARDADO_DE_2025": "Jogo Mais Aguardado de 2025 - 2 pontos",
        }

        # Renomear as colunas
        respostas_df = respostas_df.rename(columns=novo_nome_colunas)
        respostas_df_vertical = respostas_df.T

        # Título estilizado com gradiente (tamanho menor)
        st.markdown(
            """
            <h2 style='color: #ffffff; margin-top: 10px; 
            background: linear-gradient(to right, #16202c, #394e6c, #5a6f85); 
            padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; font-size: 20px;'>
                Respostas Cadastradas
            </h2>
            """,
            unsafe_allow_html=True,
        )

        # Convertendo o DataFrame transposto para HTML sem cabeçalho
        html_table = respostas_df_vertical.to_html(
            classes="dataframe", index=True, header=False, escape=False
        )

        # CSS para estilizar a tabela com foco no texto verde neon (visual mais compacto)
        css = """
        <style>
            .dataframe {
                width: 90%;  /* Tamanho da tabela menor */
                margin: 0 auto;  /* Centralizar a tabela */
                border-collapse: collapse;
                font-size: 14px;  /* Fonte menor */
                color: #ffffff;
                background-color: #16202c;
                border-radius: 8px;
            }
            .dataframe th, .dataframe td {
                padding: 8px 10px;  /* Menos espaço entre as células */
                text-align: center;
                border: 1px solid #394e6c;
                font-family: 'Arial', sans-serif;
                font-weight: bold;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);  /* Sombra mais leve */
                transition: background 0.2s ease;  /* Transição mais rápida */
            }
            .dataframe th {
                background: linear-gradient(to right, #16202c, #394e6c);
                color: #ffffff;
            }
            .dataframe tr:nth-child(even) {
                background: linear-gradient(to right, #394e6c, #5a6f85);
            }
            .dataframe tr:nth-child(odd) {
                background: linear-gradient(to right, #5a6f85, #394e6c);
            }
            .dataframe tr:hover {
                background: #394e6c;
                color: #ffffff;
            }
            .dataframe td {
                color: #39FF14; /* Verde neon */
                font-weight: bold;
                text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
            }
            .dataframe td:hover {
                background: #5a6f85;
                color: #39FF14;
                cursor: pointer;
                text-decoration: underline;
            }
            .dataframe tr:first-child th {
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            .dataframe tr:last-child td {
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)
        st.markdown(html_table, unsafe_allow_html=True)

        # AQUIIIII

        # contar_pontos(respostas_df, respostas_ganhadores_df)

    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao consultar respostas do usuário: {str(e)}")

    except Exception as ex:
        st.error(
            f"Ocorreu um erro inesperado ao consultar respostas do usuário: {str(ex)}"
        )

    finally:
        fechar_cursor(cursor)


def contar_pontos(usuario_df, respostas_ganhadores_df):
    pontos = 0
    respostas_ganhadores_df = respostas_ganhadores_df()
    usuario_lista = [
        (categoria, escolha_usuario.iloc[0])
        for categoria, escolha_usuario in usuario_df.items()
    ]

    st.markdown(
        """
        <div style='background-color: #FFFFFF; padding: 5px; border-radius: 5px; margin-top: 5px;'>
            <h2 style='color: #9932CC; text-align: center;'>Contagem de Pontos</h2>
            <p style='font-size: 16px; text-align: center; color: #000000;'>Aqui estão os resultados da contagem de pontos:</p>
        """,
        unsafe_allow_html=True,
    )

    # Criar lista de resultados para tabela
    resultados = []

    for categoria, escolha_usuario in usuario_lista:
        if categoria in respostas_ganhadores_df.columns:
            escolha_ganhador = respostas_ganhadores_df[categoria].iloc[0]
            acerto = escolha_usuario == escolha_ganhador
            pontos_categoria = obter_pontos_por_categoria(categoria) if acerto else 0

            resultados.append(
                {
                    "Categoria": categoria,
                    "Escolha do Usuário": escolha_usuario,
                    "Ganhador do Prêmio": escolha_ganhador,
                    "Resultado": "✅" if acerto else "❌",
                    "Pontos": pontos_categoria,
                }
            )

            pontos += pontos_categoria

    # Verificar se há resultados para exibir
    if not resultados:
        st.markdown(
            "<p style='font-size: 16px; text-align: center; color: #FFFFFF;'>Os resultados ainda não estão disponíveis.</p>",
            unsafe_allow_html=True,
        )
    else:
        # Criar DataFrame com os resultados
        df_resultados = pd.DataFrame(resultados)

        # Adicionar cores de fundo à tabela
        st.table(
            df_resultados.style.set_table_styles(
                [
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", "#9932CC"),
                            ("color", "#FFFFFF"),
                        ],
                    },
                    {
                        "selector": "td",
                        "props": [
                            ("background-color", "#ffffff"),
                            ("color", "#000000"),
                        ],
                    },
                    {
                        "selector": "tr:hover",
                        "props": [("background-color", "#DDA0DD")],
                    },
                ]
            )
        )
        st.markdown(
            f"<p style='font-size: 26px; margin-top: 20px; text-align: center; color: #9932CC; font-weight: bold;'>Pontuação Total: {pontos}</p>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    return pontos


def fechar_cursor(cursor):
    try:
        if cursor is not None and not cursor.is_closed():
            cursor.close()
    except Exception as e:
        st.error(f"Erro ao fechar o cursor: {str(e)}")


def verificar_e_reconectar(
    connection, account, username, password, warehouse, database, schema=None
):
    try:
        # Verifica se a conexão está fechada
        if not connection or connection.is_closed():
            st.warning("Conexão inativa. Reconectando ao Snowflake...")
            connection = conectar_snowflake(
                account, username, password, warehouse, database, schema
            )
        else:
            # Testa a conexão com um comando simples
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
    except (
        snowflake.connector.errors.ProgrammingError,
        snowflake.connector.errors.DatabaseError,
    ) as e:
        st.error(f"Erro ao verificar a conexão: {str(e)}. Tentando reconectar...")
        connection = conectar_snowflake(
            account, username, password, warehouse, database, schema
        )
    return connection


snowflake_config = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "username": "DIEGO",
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "warehouse": "COMPUTE_WH",
    "database": os.getenv("SNOWFLAKE_DATABASE"),
}


# Conecta ao Snowflake
connection = conectar_snowflake(**snowflake_config)

connection = verificar_e_reconectar(connection, **snowflake_config)

st.set_page_config(
    page_title="GOTY 2024 - Formulário",
    page_icon=":trophy:",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    cursor = connection.cursor()
    cursor.execute("SELECT CURRENT_DATE;")
    data_atual = cursor.fetchone()
    # st.write(f"Data atual no Snowflake: {data_atual[0]}")
    cursor.close()
except Exception as e:
    st.error(f"Erro ao executar consulta: {str(e)}")
