import streamlit as st



class Sidebar:
    def __init__(self):
        pass

    def render(self):
        st.header("Informações")
        st.markdown("""
        ### Sobre o Sistema
        Este sistema utiliza blockchain para armazenar hashes de informações de produtos para garantir a sua autenticidade.
        
        ### Características
        - Armazenamento apenas de hashes e suas informações
        - Validação de integridade da blockchain
        - Interface interativa e responsiva
        - Autenticação de produtos manualmente e via QR Code 
        
        ### Como usar
        1. **Registro**: Cadastre um produto inserindo suas informações
        2. **Autenticação**: Verifique a autenticidade com seu nome e número de identificação ou com o uso do QR Code
        3. **Blockchain**: Explore todos os blocos registrados na blockchain
        """)
        
        # Estatísticas da blockchain
        st.metric("Total de Blocos", len(st.session_state.blockchain.blocks))
        st.metric("Dificuldade de Mineração", st.session_state.blockchain.difficulty) 