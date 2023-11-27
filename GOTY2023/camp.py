import pandas as pd
import streamlit as st
import re
import snowflake.connector
from snowflake.connector import ProgrammingError
from pontuacoes import obter_categorias_escolhidas, obter_pontos_por_categoria, respostas_ganhadores_df
from datetime import datetime

# Constantes
TABELA_PADRAO = "GOTY2023"
cursor = None

#Funciona o deleta do usuario. 
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
            st.warning("Não é permitido excluir dados após 07/12/2023.")
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
    <div style='background: linear-gradient(to right, #ff9900, #f2f2f2); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: #ff3300; text-align: center;'>
            <img src='https://medlimp.com.br/wp-content/uploads/2023/03/LIXEIRA-BRANCA-50L-SEM-POSTE-COM-HASTE-METALICA-JSN.png' style='vertical-align: middle; height: 1em;'/> Excluir Dados do Usuário
        </h1>
        <p style='color: #666666; font-size: 16px; text-align: center; background: linear-gradient(to right, #f2f2f2, #ffffff); padding: 15px; border-radius: 8px;'>
            🚨 <strong>Aviso:</strong> A exclusão de dados é uma ação irreversível. Utilize esta opção apenas para corrigir informações incorretas
            ou refazer seu formulário. A exclusão não será possível após a data limite.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


    col1, col2, col3 = st.columns(3)
    with col1:
        email_exclusao = st.text_input("Email:")
    with col2:
        nome_exclusao = st.text_input("Nome:")
    with col3:
        telegram_exclusao = st.text_input("Nome no Telegram:")

    if st.button("Excluir Meus Dados"):
        apagar_dados_usuario(connection, 'GOTY2023', email_exclusao, nome_exclusao, telegram_exclusao)



# Funções de Conexão
def conectar_snowflake(account, username, password, warehouse, database, schema=None):
    try:
        connection = snowflake.connector.connect(
            user=username,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        return connection
    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao conectar ao Snowflake: {str(e)}")
        return None

# Funções de Verificação
def verificar_existencia_usuario(connection, email=None, nome=None, telegram=None, tabela=TABELA_PADRAO):
    cursor = None  # Inicializa cursor fora do bloco try
    try:
        cursor = connection.cursor()
        if not tabela_existe(cursor, tabela):
            st.warning(f"A tabela '{tabela}' não existe.")
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
            st.warning("⚠️ Você já preencheu o formulário. Não é permitido preencher novamente. Você pode apagar sua aposta atual até o dia 02/11/2023, caso queira preencher de novo.")
            return
        colunas_categorias = [
            re.sub(r'[^a-zA-Z0-9_]', '_', categoria.split('-')[0].strip())
            for categoria in respostas_usuario.keys()
        ]
        colunas_query = ', '.join(colunas_categorias)
        placeholders = ', '.join(['%s' for _ in respostas_usuario.values()])
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
                re.sub(r'[^a-zA-Z0-9_]', '_', categoria_info['Categoria'].split('-')[0].strip())
                for categoria_info in categorias_escolhidas.values()
            ]

            query = f'''
                CREATE TABLE IF NOT EXISTS public.{tabela} (
                    email STRING,
                    nome STRING,
                    telegram STRING,
                    {' STRING, '.join(colunas_categorias)} STRING
                );
            '''
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
    <h1 style='color: #ffffff; text-align: center; background: linear-gradient(to right, #ff9900, #ff3300); padding: 5px; border-radius: 11px;'>
        <img src='https://cdn.worldvectorlogo.com/logos/the-game-awards.svg' style='vertical-align: middle; height: 1em;'/> Votação - The Game Awards
    </h1>
    <div style='background: linear-gradient(to right, #ff9900, #f2f2f2); padding: 20px; border-radius: 10px;'>
        <p style='color: #000000; font-size: 16px; text-align: center; background: linear-gradient(to right, #f2f2f2, #ffffff); padding: 15px; border-radius: 8px;'>
            🎮 Bem-vindo ao Formulário de Votação do The Game Awards! Este é um evento descontraído entre amigos.
            Os resultados serão anunciados em 7 de Dezembro de 2023. Boa sorte!
            Para discussões e mais informações, participe do nosso grupo no 
            <a href='https://t.me/seu_grupo_do_telegram' target='_blank' style='color: #0099cc;'>
                <img src='https://img.icons8.com/color/24/000000/telegram-app--v5.png' alt='Telegram'/>
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
        st.warning("Você já preencheu o formulário. Não é permitido preencher novamente.")
        return
    
    respostas_usuario = obter_respostas_usuario(categorias_escolhidas)
    exibir_escolhas_usuario(respostas_usuario)
    if st.button("Confirmar e Salvar Respostas"):
        criar_tabela_sql(connection, "GOTY2023", categorias_escolhidas)
        inserir_dados_usuario(connection, "GOTY2023", email, nome, telegram, respostas_usuario)


# Funções Auxiliares
def obter_respostas_usuario(categorias_escolhidas):
    respostas_usuario = {}

    for numero, categoria_info in categorias_escolhidas.items():
        categoria = categoria_info["Categoria"]
        opcoes = categoria_info["Opções"]

        if st.checkbox(f"{numero}. Escolher {categoria}", key=categoria):
            st.write("Clique abaixo para ver as opções:")
            with st.expander(f"Opções para {categoria}", expanded=False):
                opcao_escolhida = st.selectbox(f"Escolha a opção em {categoria}:", opcoes)
                respostas_usuario[categoria] = opcao_escolhida
            st.markdown('<div style="float: right; margin-right: 20px;"><span style="color:green">&#10004;</span> Categoria escolhida: {}</div>'.format(categoria), unsafe_allow_html=True)
    escolhas_usuario_dict = {categoria: opcao for categoria, opcao in respostas_usuario.items()}
    escolhas_usuario_df = pd.DataFrame.from_dict(escolhas_usuario_dict, orient='index', columns=["Escolha"])

    return respostas_usuario



def exibir_escolhas_usuario(categorias_escolhidas):
    st.markdown(
        "<h2 style='color: #ffffff; margin-top: 20px; background: linear-gradient(to right, #333333, #ff6600); padding: 15px; border-radius: 8px; text-align: center; font-weight: bold;'>Visualização das Suas Escolhas</h2>",
        unsafe_allow_html=True
    )
    escolhas_usuario_df = pd.DataFrame.from_dict(categorias_escolhidas, orient='index', columns=["Escolha"])
    escolhas_usuario_df = escolhas_usuario_df.T
    estilo_df = {
        "selector": "th",
        "props": [("background-color", "#333333"), ("color", "#ff6600")]
    }
    st.dataframe(escolhas_usuario_df.style
        .set_table_styles([estilo_df])
        .apply(lambda x: ["background: linear-gradient(to right, #333333, #666666); color: #ff6600"] * len(x), axis=1)
    )

def exibir_formulario_visualizacao_respostas():
    st.markdown(
        """
        <div style='background: linear-gradient(to right, #ff9900, #f2f2f2); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: #ff3300; text-align: center;'>
                <img src='https://cdn3.iconfinder.com/data/icons/web-and-seo-31/16/invisible-eye-512.png' style='vertical-align: middle; height: 1em;'/> Visualizar Respostas
            </h1>
            <p style='color: #666666; font-size: 16px; text-align: center; background: linear-gradient(to right, #f2f2f2, #ffffff); padding: 15px; border-radius: 8px;'>
                📋 Aqui você pode visualizar suas respostas cadastradas no formulário. No dia do evento, você saberá quantos pontos acumulou com suas escolhas!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email:")
    with col2:
        telegram = st.text_input("Nome no Telegram:")

    if st.button("Visualizar Respostas"):
        visualizar_respostas_usuario(email, telegram, connection, 'GOTY2023')


# Função para visualizar as respostas do usuário
def visualizar_respostas_usuario(email, telegram, connection, tabela):
    try:
        cursor = connection.cursor()

        # Verificar se a tabela existe
        if not tabela_existe(cursor, tabela):
            st.warning(f"A tabela '{tabela}' não existe.")
            return

        # Verificar se o usuário existe
        if not verificar_existencia_usuario(connection, email, telegram=telegram, tabela=tabela):
            st.warning("Usuário não encontrado. Nenhuma resposta disponível.")
            return

        # Consultar as respostas do usuário
        query = f"SELECT * FROM {tabela} WHERE Email = %s AND Telegram = %s"
        cursor.execute(query, (email, telegram))
        usuario_respostas = cursor.fetchone()

        # Criar um DataFrame com as respostas do usuário
        respostas_df = pd.DataFrame([usuario_respostas], columns=[desc[0] for desc in cursor.description])

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
            "MELHOR_SUPORTE_COMUNIT_RIO": "Melhor Suporte Comunitário - 3 pontos",
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
            "JOGO_MAIS_AGUARDADO_DE_2024": "Jogo Mais Aguardado de 2024 - 2 pontos"
        }

        # Renomear as colunas
        respostas_df = respostas_df.rename(columns=novo_nome_colunas)
        st.markdown(
            """
            <h2 style='color: #ffffff; margin-top: 20px; background: linear-gradient(to right, #333333, #ff6600); padding: 15px; border-radius: 8px; text-align: center; font-weight: bold;'>Respostas Cadastradas</h2>
            """,
            unsafe_allow_html=True)
        st.dataframe(respostas_df.style
            .set_table_styles([{"selector": "th", "props": [("background-color", "#333333"), ("color", "#ff6600")]}])
            .apply(lambda x: ["background: linear-gradient(to right, #333333, #666666); color: #ff6600"] * len(x), axis=1)
        )
        contar_pontos(respostas_df, respostas_ganhadores_df)

    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Erro ao consultar respostas do usuário: {str(e)}")

    except Exception as ex:
        st.error(f"Ocorreu um erro inesperado ao consultar respostas do usuário: {str(ex)}")

    finally:
        fechar_cursor(cursor)




def contar_pontos(usuario_df, respostas_ganhadores_df):
    pontos = 0
    respostas_ganhadores_df = respostas_ganhadores_df()
    usuario_lista = [(categoria, escolha_usuario.iloc[0]) for categoria, escolha_usuario in usuario_df.items()]

    st.markdown("<h2 style='color: #ff6600;'>Contagem de Pontos</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px;'>Aqui estão os resultados da contagem de pontos:</p>", unsafe_allow_html=True)

    for categoria, escolha_usuario in usuario_lista:
        if categoria in respostas_ganhadores_df.columns:
            escolha_ganhador = respostas_ganhadores_df[categoria].iloc[0]
            if escolha_usuario == escolha_ganhador:
                pontos += obter_pontos_por_categoria(categoria)
                st.markdown(f"<p style='color: #00cc00; font-size: 14px;'>✅ {categoria}: {escolha_usuario} (GOTY2023)</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color: #ff0000; font-size: 14px;'>❌ {categoria}: {escolha_usuario} (GOTY2023)</p>", unsafe_allow_html=True)

    st.markdown(f"<p style='font-size: 18px; margin-top: 20px;'>Pontos totais: <span style='color: #ff6600;'>{pontos}</span></p>", unsafe_allow_html=True)
    return pontos

def fechar_cursor(cursor):
    try:
        if cursor is not None and not cursor.is_closed():
            cursor.close()
    except Exception as e:
        st.error(f"Erro ao fechar o cursor: {str(e)}")


snowflake_credentials = st.secrets["snowflake_credentials"]

# Conecta ao Snowflake
connection = conectar_snowflake(**snowflake_credentials)



# Executa o aplicativo Streamlit
if __name__ == "__main__":
    exibir_formulario()
