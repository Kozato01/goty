import streamlit as st
from camp import exibir_formulario, exibir_formulario_exclusao, exibir_formulario_visualizacao_respostas

def definir_estilo_pagina():
    estilo = """
        <style>
            body {
                font-size: 17px; /* Ajuste o tamanho do texto conforme necessário */
            }

            .stApp > header {
                background-color: transparent;
            }

            .stApp {
                margin: auto;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                overflow: auto;
                background: linear-gradient(to bottom, #C5E0FF, #76a8f5, #9D28BD); /* Cores do degradê de fundo */
                background-size: cover;
                background-attachment: fixed;
                color: #000000; /* Cor do texto, ajustada para preto */
            }

            .css-1aumxhk {
                color: #000000 !important; /* Cor do texto do sidebar, ajustada para preto */
            }

            .st-d7 .st-ek.st-d4, .st-ee.st-d4 {
                color: #000000; /* Cor do texto no tema claro, ajustada para preto */
                background-color: #FFFFFF; /* Cor de fundo no tema claro, ajustada para branco */
            }

            .st-d7 .st-ek.st-d4 button, .st-ee.st-d4 button {
                background-color: #008080; /* Cor do botão no tema claro, ajustada para verde azulado */
                color: #FFFFFF; /* Cor do texto no botão no tema claro, ajustada para branco */
            }

            .st-d7 .st-ek.st-d4 button:hover, .st-ee.st-d4 button:hover {
                background-color: #006666; /* Cor do botão (hover) no tema claro, ajustada para tom mais escuro de verde azulado */
            }

            /* Estilos específicos para o tema escuro */
            .st-d7 button {
                background-color: #008080; /* Cor do botão no tema escuro, ajustada para cinza escuro */
                color: #FFFFFF; /* Cor do texto no botão no tema escuro, ajustada para branco */
            }

            .st-d7 button:hover {
                background-color: #555555; /* Cor do botão (hover) no tema escuro, ajustada para cinza mais claro */
            }
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

def main():
    definir_estilo_pagina()

    # Adicionar links para páginas
    st.sidebar.markdown("<h3 style='color: #000000;'>Navegação:</h3>", unsafe_allow_html=True)
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
