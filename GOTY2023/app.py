import streamlit as st
from utils import Resultado, visualizar_respostas, exibir_formulario, baixar_respostas_usuario

# Adicionar degradê ao fundo
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom, #282c35, #3e4451, #282c35) !important;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
        margin: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }
    h1 {
        color: #ff6600;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    p {
        color: #ff6600;
        font-size: 18px;
        text-align: center;
    }
    a {
        color: #ff6600;
    }
    h3 {
        color: #ff6600;
        text-align: center;
    }
    .sidebar-content {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Adicionar estilo ao título
    st.markdown("<h1>Formulário de Votação - The Game Awards</h1>", unsafe_allow_html=True)

    # Adicionar informações sobre o evento na página de Formulário
    if "page" not in st.session_state:
        st.session_state.page = "Formulário"

    if st.session_state.page == "Formulário":
        st.markdown(
            """
            <p>
                Bem-vindo ao Formulário de Votação do The Game Awards! Este é um evento descontraído entre amigos.
                Os resultados serão anunciados em 7 de Dezembro 2023. Boa sorte! 
                <a href='https://t.me/seu_grupo_do_telegram' target='_blank'>
                    <img src='https://img.icons8.com/color/48/000000/telegram-app--v5.png' alt='Telegram'/>
                </a>
            </p>
            """,
            unsafe_allow_html=True,
        )

        # Adicionar links para páginas
        st.sidebar.markdown("<h3>Navegação:</h3>", unsafe_allow_html=True)
        page = st.sidebar.radio("", ["Formulário", "Visualizar Respostas"], key="sidebar")

        if page == "Formulário":
            exibir_formulario()
        elif page == "Visualizar Respostas":
            col1, col2 = st.columns(2)
            with col1:
                email_visualizar = st.text_input("Email:").lower()
            with col2:
                nome_visualizar = st.text_input("Nome:").lower()
            if st.button("Visualizar Respostas"):
                respostas_ganhadores_df = Resultado()
                visualizar_respostas(email_visualizar, nome_visualizar, respostas_ganhadores_df=None)
    elif st.session_state.page == "Visualizar Respostas":
        st.markdown(
            """
            <p>
                Visualize suas respostas do Formulário do The Game Awards.
            </p>
            """,
            unsafe_allow_html=True,
        )
        
        st.subheader("Visualizar suas respostas:")
        col1, col2 = st.columns(2)
        with col1:
            email_visualizar = st.text_input("Email:").lower()
        with col2:
            nome_visualizar = st.text_input("Nome:").lower()
        if st.button("Visualizar Respostas"):
            respostas_ganhadores_df = Resultado()
            visualizar_respostas(email_visualizar, nome_visualizar, respostas_ganhadores_df=None)


if __name__ == "__main__":
    main()
