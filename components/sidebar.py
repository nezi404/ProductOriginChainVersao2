import streamlit as st
from datetime import datetime

class Sidebar:
    def __init__(self):
        pass

    def render(self):
        st.header("Informações")
        st.markdown("""
        ### Sobre o Sistema
        O **ProductsOriginChain** é uma aplicação que utiliza tecnologia blockchain para ajudar empresas e consumidores a garantir a **autenticidade de produtos**. Através de um QR Code gerado no momento do registro, qualquer pessoa pode verificar se um produto foi de fato registrado por uma empresa autorizada.
        
        ### Características
        - Registros imutáveis e descentralizados usando blockchain
        - Geração de QR Code para verificação rápida
        - Apenas empresas autorizadas podem registrar produtos
        - Interface simples e intuitiva feita com Streamlit
        
        ### Como usar
        1. **Empresas**: Acesse a aba "Registrar Produto", preencha os dados e gere o QR Code.
        2. **Consumidores**: Acesse a aba "Verificar Produto" e escaneie ou digite o código do QR Code.
        3. **Blockchain**: Explore os blocos de produtos registrados e valide a integridade da cadeia.
        """)
        
        # Estatísticas da blockchain
        st.metric("Total de Blocos", len(st.session_state.blockchain.blocks))
        st.metric("Dificuldade de Mineração", st.session_state.blockchain.difficulty) 