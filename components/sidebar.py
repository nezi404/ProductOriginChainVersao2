import json
import streamlit as st
import hashlib
from datetime import datetime
import os
from PIL import Image
import qrcode
import base64
import io
import uuid

class Sidebar:
    def __init__(self):
        pass

    def render(self):
        st.header("Informações")
        st.markdown("""
        ### Sobre o Sistema
        Este sistema utiliza blockchain para armazenar hashes de impressões digitais de forma segura e imutável.
        
        ### Características
        - Armazenamento apenas de hashes (não das imagens originais)
        - Validação de integridade da blockchain
        - Interface interativa e responsiva
        - Autenticação biométrica segura
        
        ### Como usar
        1. **Registro**: Cadastre uma nova impressão digital
        2. **Autenticação**: Verifique a identidade com impressão digital
        3. **Blockchain**: Explore todos os blocos registrados
        """)
        
        # Estatísticas da blockchain
        st.metric("Total de Blocos", len(st.session_state.blockchain.blocks))
        st.metric("Dificuldade de Mineração", st.session_state.blockchain.difficulty) 