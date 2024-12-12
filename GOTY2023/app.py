import streamlit as st
from camp import (
    exibir_formulario,
    exibir_formulario_exclusao,
    exibir_formulario_visualizacao_respostas,
)
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


def definir_estilo_pagina():
    cor_laranja_claro = "#16202c"
    cor_laranja_escuro = "#394e6c"
    cor_branco = "#16202c"

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
                color: #FFFFFF !important; /* Cor do texto do sidebar, ajustada para branco */
            }}

            .st-d7 .st-ek.st-d4 button, .st-ee.st-d4 button {{
                background-color: {cor_laranja_claro}; /* Cor do botão no tema claro */
                color: {cor_branco}; /* Cor do texto no botão no tema claro, ajustada para branco */
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }}
            
            button[kind="secondary"] {{
            background-color: #FFFFFF !important; /* Fundo branco */
            font-weight: bold !important; /* Texto em negrito */
            border: 1px solid {cor_laranja_claro}; /* Borda opcional */
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            transition: background-color 0.3s ease, transform 0.2s ease;
            }}

        button[kind="secondary"]:hover {{
            background-color: {cor_laranja_claro}; /* Fundo alterado no hover */
            transform: scale(1.05); /* Efeito de aumento no hover */
             }}

            .st-d7 .st-ek.st-d4 button:hover, .st-ee.st-d4 button:hover {{
                background-color: {cor_laranja_escuro}; /* Cor do botão (hover) no tema claro */
                color: {cor_branco};
                transform: scale(1.05); /* Efeito de aumento no hover */
            }}

            /* Estilos específicos para o tema escuro */
            .st-d7 button {{
                background-color: {cor_laranja_claro}; /* Cor do botão no tema escuro */
                color: {cor_branco}; /* Cor do texto no botão no tema escuro */
            }}

            .st-d7 button:hover {{
                background-color: {cor_laranja_escuro}; /* Cor do botão (hover) no tema escuro */
                color: {cor_branco};
                transform: scale(1.05); /* Efeito de aumento no hover */
            }}

            /* Estilo para links */
            a {{
                color: {cor_laranja_escuro};
                text-decoration: none;
                transition: color 0.3s ease;
            }}

            a:hover {{
                color: {cor_laranja_claro};
            }}

            /* Estilos para textos importantes */
            h1, h2, h3 {{
                color: {cor_laranja_escuro};
            }}
        </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    definir_estilo_pagina()

    # Título do menu de navegação
    st.sidebar.markdown(
        "<h2 style='color: #e9e3fa; text-align: center;'>Menu</h2>",
        unsafe_allow_html=True,
    )

    # Opções de navegação
    page = st.sidebar.selectbox(
        "Escolha uma opção:",
        # ["Formulário", "Visualizar Respostas", "Excluir Dados"],
        ["Visualizar Respostas"],
        key="sidebar_menu",
    )

    # Exibe as páginas com base na seleção
    # if page == "Formulário":
    #    exibir_formulario()

    if page == "Visualizar Respostas":
        exibir_formulario_visualizacao_respostas()

    # elif page == "Excluir Dados":
    #   exibir_formulario_exclusao()


if __name__ == "__main__":
    main()
