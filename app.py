import json
import streamlit as st
from services.blockchain import Blockchain
from services.product_data import ProductData
from components.register_product import RegisterProduct
from components.verify_product import VerifyProduct
from components.product_history import ProductsHistory
from components.sidebar import Sidebar
from datetime import datetime
from PIL import Image


class App:

    def run():
        # Configuração da página
        st.set_page_config(
            page_title="Blockchain de autenticidade de produtos eletrônicos",
            page_icon="🔒",
            layout="wide"
        )

        # Inicialização da blockchain (usando session_state para persistir entre reruns)
        if 'blockchain' not in st.session_state:
            st.session_state.blockchain = Blockchain(difficulty=4)

        # Estado para controlar qual aba está ativa
        if 'tab' not in st.session_state:
            st.session_state.tab = "registro"

        # Título principal
        st.title("🔒 Blockchain de Autenticidade de Produtos")

        # Tabs para navegação
        tabs = ["Registro", "Autenticação", "Blockchain"]
        selected_tab = st.radio("Selecione uma opção:", tabs, horizontal=True)

        if selected_tab == "Registro":
            register_page = RegisterProduct()
            register_page.render()

        elif selected_tab == "Autenticação":
            verify_page = VerifyProduct()
            verify_page.render()

        elif selected_tab == "Blockchain":
            history_page = ProductsHistory()
            history_page.render()

        # Sidebar com informações adicionais
        with st.sidebar:
            sidebar = Sidebar()
            sidebar.render()

App.run()