import streamlit as st
from camp import exibir_formulario, exibir_formulario_exclusao, exibir_formulario_visualizacao_respostas
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def definir_estilo_pagina():
    # Definindo variáveis para as cores principais
    cor_laranja_claro = "#FF8247"
    cor_laranja_escuro = "#ffc9b0"  # Tom mais escuro de laranja
    cor_branco = "#FFFFFF"

    # Estilo da página
    estilo = f"""
        <style>
            body {{
                font-size: 17px; /* Ajuste o tamanho do texto conforme necessário */
            }}

            .stApp > header {{
                background-color: transparent;
            }}

            .stApp {{
                margin: auto;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                overflow: auto;
                background: linear-gradient(to bottom, {cor_laranja_claro}, {cor_laranja_escuro}, {cor_branco});
                color: #000000; /* Cor do texto, ajustada para preto */
            }}

            .css-1aumxhk {{
                color: {cor_branco} !important; /* Cor do texto do sidebar, ajustada para branco */
            }}

            .st-d7 .st-ek.st-d4 button, .st-ee.st-d4 button {{
                background-color: #FF6347; /* Cor do botão no tema claro, tom mais escuro de laranja */
                color: {cor_branco}; /* Cor do texto no botão no tema claro, ajustada para branco */
            }}

            .st-d7 .st-ek.st-d4 button:hover, .st-ee.st-d4 button:hover {{
                background-color: #FF4500; /* Cor do botão (hover) no tema claro, tom mais intenso de laranja */
                color: {cor_branco}; /* Cor do texto no botão (hover) no tema claro, ajustada para branco */
            }}

            /* Estilos específicos para o tema escuro */
            .st-d7 button {{
                background-color: #FF6347; /* Cor do botão no tema escuro, tom mais escuro de laranja */
                color: {cor_branco}; /* Cor do texto no botão no tema escuro, ajustada para branco */
            }}

            .st-d7 button:hover {{
                background-color: #FF4500; /* Cor do botão (hover) no tema escuro, tom mais intenso de laranja */
                color: {cor_branco}; /* Cor do texto no botão (hover) no tema escuro, ajustada para branco */
            }}
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

def main():
    definir_estilo_pagina()

    # Adicionar links para páginas
    st.sidebar.markdown("<h3 style='color: #e54747;'>Navegação:</h3>", unsafe_allow_html=True)
    page = st.sidebar.radio("", ["Formulário", "Visualizar Respostas", "Excluir Dados"], key="sidebar")

    if page == "Formulário":
        exibir_formulario()

    elif page == "Visualizar Respostas":
        exibir_formulario_visualizacao_respostas()

    elif page == "Excluir Dados":
        exibir_formulario_exclusao()

if __name__ == "__main__":
    st.set_page_config(
        page_title="GOTY 2023 - Formulário",
        page_icon=":trophy:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
