import streamlit as st
from utils import exibir_formulario, exibir_formulario_exclusao, exibir_formulario_visualizacao_respostas

def definir_estilo_pagina():
    estilo = """
        <style>
            .stApp > header {
                background-color: transparent;
            }

            .stApp {
                margin: auto;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                overflow: auto;
                background: linear-gradient(315deg, #001f3f 0%, #ff851b 100%);
                background-size: cover;
                background-attachment: fixed;
                color: #ffffff; /* Cor do texto */
            }
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="GOTY 2023 - Formulário",
        page_icon=":trophy:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    definir_estilo_pagina()

    # Adicionar links para páginas
    st.sidebar.markdown("<h3 style='color: #ffffff;'>Navegação:</h3>", unsafe_allow_html=True)
    page = st.sidebar.radio("", ["Formulário", "Visualizar Respostas", "Excluir Dados"], key="sidebar")

    if page == "Formulário":
        exibir_formulario()

    elif page == "Visualizar Respostas":
        exibir_formulario_visualizacao_respostas()
        pass

    elif page == "Excluir Dados":
        exibir_formulario_exclusao()

if __name__ == "__main__":
    main()
