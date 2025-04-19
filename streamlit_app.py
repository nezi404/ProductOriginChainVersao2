import streamlit as st
from blockchain import Blockchain
from biometric_data import BiometricData
import hashlib
from datetime import datetime
import os
from PIL import Image
import io

# Configuração da página
st.set_page_config(
    page_title="Blockchain de Impressões Digitais",
    page_icon="🔒",
    layout="wide"
)

# Inicialização da blockchain (usando session_state para persistir entre reruns)
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain(difficulty=4)

# Estado para controlar qual aba está ativa
if 'tab' not in st.session_state:
    st.session_state.tab = "registro"

def hash_fingerprint_image(image_data):
    """
    Gera um hash da imagem da impressão digital
    """
    return hashlib.sha256(image_data).hexdigest()

def process_fingerprint(image, person_id):
    """
    Processa a imagem da impressão digital e adiciona à blockchain
    """
    try:
        # Converter a imagem para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Gerar hash da imagem
        fingerprint_hash = hash_fingerprint_image(img_byte_arr)
        
        # Criar dados biométricos
        biometric_data = BiometricData(
            fingerprint_hash=fingerprint_hash,
            person_id=person_id,
            capture_date=datetime.now().isoformat(),
            quality_score=95  # Em um caso real, isso seria calculado baseado na qualidade da imagem
        )
        
        # Adicionar à blockchain
        new_block = st.session_state.blockchain.new_block(biometric_data)
        st.session_state.blockchain.add_block(new_block)
        
        return True, "Impressão digital registrada com sucesso!", new_block
    except Exception as e:
        return False, f"Erro ao processar impressão digital: {str(e)}", None

def verify_fingerprint(image, person_id):
    """
    Verifica se a impressão digital existe na blockchain para o ID da pessoa
    """
    try:
        # Converter a imagem para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Gerar hash da impressão digital
        fingerprint_hash = hash_fingerprint_image(img_byte_arr)
        
        # Procurar na blockchain por uma correspondência
        for block in st.session_state.blockchain.blocks:
            if hasattr(block.data, 'to_json') and isinstance(block.data, BiometricData):
                # Verificar se o hash e o ID da pessoa correspondem
                if (block.data.fingerprint_hash == fingerprint_hash and 
                    block.data.person_id == person_id):
                    return True, block
        
        return False, None
    except Exception as e:
        st.error(f"Erro ao verificar impressão digital: {str(e)}")
        return False, None

# Título principal
st.title("🔒 Blockchain de Impressões Digitais")

# Tabs para navegação
tabs = ["Registro", "Autenticação", "Blockchain"]
selected_tab = st.radio("Selecione uma opção:", tabs, horizontal=True)

if selected_tab == "Registro":
    st.header("Registrar Nova Impressão Digital")
    
    # Formulário de upload
    with st.form("fingerprint_form"):
        person_id = st.text_input("ID da Pessoa", key="person_id")
        uploaded_file = st.file_uploader("Selecione a imagem da impressão digital", 
                                      type=['png', 'jpg', 'jpeg', 'bmp'],
                                      key="fingerprint")
        
        # Preview da imagem
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview da Impressão Digital", use_column_width=True)
        
        submitted = st.form_submit_button("Registrar na Blockchain")
        
        if submitted:
            if not person_id:
                st.error("Por favor, insira o ID da pessoa")
            elif uploaded_file is None:
                st.error("Por favor, selecione uma imagem")
            else:
                success, message, block = process_fingerprint(image, person_id)
                if success:
                    st.success(message)
                    st.info(f"Hash do bloco: {block.hash}")
                else:
                    st.error(message)

elif selected_tab == "Autenticação":
    st.header("Autenticar com Impressão Digital")
    
    with st.form("auth_form"):
        auth_person_id = st.text_input("ID da Pessoa", key="auth_person_id")
        auth_file = st.file_uploader("Selecione a imagem da impressão digital", 
                                   type=['png', 'jpg', 'jpeg', 'bmp'],
                                   key="auth_fingerprint")
        
        # Preview da imagem
        if auth_file is not None:
            auth_image = Image.open(auth_file)
            st.image(auth_image, caption="Impressão Digital para Autenticação", use_column_width=True)
        
        auth_submitted = st.form_submit_button("Verificar Identidade")
        
        if auth_submitted:
            if not auth_person_id:
                st.error("Por favor, insira o ID da pessoa")
            elif auth_file is None:
                st.error("Por favor, selecione uma imagem")
            else:
                with st.spinner("Verificando impressão digital..."):
                    is_match, matching_block = verify_fingerprint(auth_image, auth_person_id)
                    
                    if is_match:
                        st.success("✅ Autenticação bem-sucedida!")
                        st.balloons()
                        
                        # Mostrar detalhes do registro
                        st.subheader("Detalhes do Registro")
                        st.info(f"""
                        **ID da Pessoa:** {matching_block.data.person_id}  
                        **Data de Registro:** {matching_block.data.capture_date}  
                        **Qualidade:** {matching_block.data.quality_score}/100  
                        **Bloco:** #{matching_block.index}  
                        **Hash do Bloco:** {matching_block.hash[:20]}...
                        """)
                    else:
                        st.error("❌ Autenticação falhou. Impressão digital não encontrada para este ID.")

elif selected_tab == "Blockchain":
    st.header("Estado da Blockchain")
    
    # Exibir status da blockchain
    is_valid = st.session_state.blockchain.is_blockchain_valid()
    if is_valid:
        st.success("✅ Blockchain válida")
    else:
        st.error("❌ Blockchain inválida")
    
    # Exibir blocos
    st.subheader("Blocos da Blockchain")
    
    # Criar um container com altura fixa e scroll
    blockchain_container = st.container()
    
    with blockchain_container:
        for block in st.session_state.blockchain.blocks:
            with st.expander(f"Bloco #{block.index}", expanded=True):
                st.markdown(f"""
                **Hash Anterior:** `{block.previous_hash}`  
                **Timestamp:** {datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')}  
                **Hash:** `{block.hash}`  
                **Dados:** {block.data}
                """)
                st.markdown("---")

# Sidebar com informações adicionais
with st.sidebar:
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