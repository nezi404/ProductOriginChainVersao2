import json
import streamlit as st
from blockchain import Blockchain
from product_data import ProductData
import hashlib
from datetime import datetime
import os
from PIL import Image
import qrcode
import base64
import io

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

def hash_product_qrcode_image(image):
    """
    Gera um hash da imagem da impressão digital
    """
    return hashlib.sha256(image).hexdigest()

def process_product(product_name,
                    batch_number,
                    manufacture_date, 
                    manufacturer,
                    manufacturing_location,
                    brief_description
                    ):
    """
    Processa a imagem da impressão digital e adiciona à blockchain
    """
    try:
        # # Converter a imagem para bytes
        # img_byte_arr = io.BytesIO()
        # image.save(img_byte_arr, format=image.format)
        # img_byte_arr = img_byte_arr.getvalue()
        
        # # Gerar hash da imagem
        # fingerprint_hash = hash_fingerprint_image(img_byte_arr)
        
        # Criar dados biométricos
        product_data = ProductData(
            # fingerprint_hash=fingerprint_hash,
            product_name =  product_name,
            batch_number = batch_number,
            manufacture_date = manufacture_date, 
            manufacturer = manufacturer,
            manufacturing_location = manufacturing_location,
            brief_description = brief_description,
            capture_date=datetime.now().isoformat(),
            # quality_score=95  # Em um caso real, isso seria calculado baseado na qualidade da imagem
        )
        
        # Adicionar à blockchain
        new_block = st.session_state.blockchain.new_block(product_data)
        st.session_state.blockchain.add_block(new_block)
        
        return True, "Produto registrado com sucesso!", new_block
    except Exception as e:
        return False, f"Erro ao processar produto: {str(e)}", None

def verify_product(image):
    """
    Verifica se a impressão digital existe na blockchain para o ID da pessoa
    """
    try:
        # Converter a imagem para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Gerar hash da impressão digital
        product_hash = hash_product_qrcode_image(img_byte_arr)
        
        # Procurar na blockchain por uma correspondência
        for block in st.session_state.blockchain.blocks:
            if hasattr(block.data, 'to_json') and isinstance(block.data, ProductData):
                # Verificar se o hash e o ID da pessoa correspondem
                if (block.data.product_hash == product_hash):
                    return True, block
        
        return False, None
    except Exception as e:
        st.error(f"Erro ao verificar autenticidade do produto: {str(e)}")
        return False, None

# Título principal
st.title("🔒 Blockchain de Autenticidade de Produtos")

# Tabs para navegação
tabs = ["Registro", "Autenticação", "Blockchain"]
selected_tab = st.radio("Selecione uma opção:", tabs, horizontal=True)

if selected_tab == "Registro":
    st.header("Registrar Novo Produto")

    # CSS para alinhar os botões à direita
    st.markdown("""
        <style>
            .css-button-container {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Formulário de upload
    with st.form("product_form"):
        # Criação das duas colunas
        col1, col2 = st.columns(2)

        # Preenchendo a primeira coluna com os campos
        with col1:
            product_name = st.text_input("Nome do produto", key="product_name")
            batch_number = st.text_input("Número do lote", key="batch_number")
            manufacture_date = st.text_input("Data de fabricação", key="manufacture_date")

        # Preenchendo a segunda coluna com os campos
        with col2:
            manufacturer = st.text_input("Fabricante", key="manufacturer")
            manufacturing_location = st.text_input("Local de fabricação", key="manufacturing_location")
            brief_description = st.text_input("Descrição breve", key="brief_description")


        # botões alinhados à direita
        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([6, 1, 1])
        with col3:
            submitted = st.form_submit_button("Registrar na Blockchain")
        with col3:
            # Remover o botão 'Limpar Campos' de dentro do formulário
            st.markdown('</div>', unsafe_allow_html=True)

    # GERA IMAGEM DE TESTES
    def generate_qrcode(data_dict):
        data_str = json.dumps(data_dict, indent=2)
        qr = qrcode.make(data_str)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        buf.seek(0)
        return buf

    if submitted:
        if not all([product_name, batch_number, manufacture_date, manufacturer, manufacturing_location, brief_description]):
            st.error("Por favor, Preencha todos os campos")
        else:
            success, message, block = process_product(
                product_name,
                batch_number,
                manufacture_date, 
                manufacturer,
                manufacturing_location,
                brief_description
                )
            if success:
                st.success(message)
                # st.info(f"Hash do bloco: {block.hash}")

                qr_code_img = generate_qrcode({
                    "product_name": product_name,
                    "batch_number": batch_number,
                    "manufacture_date": manufacture_date,
                    "manufacturer": manufacturer,
                    "location": manufacturing_location,
                    "description": brief_description,
                    "block_hash": block.hash
                })

                # Converta a imagem para base64
                qr_code_base64 = base64.b64encode(qr_code_img.read()).decode("utf-8")
                qr_code_img.seek(0)  # volta pro começo, caso ainda precise usá-la depois

                # Insere HTML com imagem centralizada e tamanho ajustado
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="data:image/png;base64,{qr_code_base64}" width="300"/>
                        <p style="font-size: 14px;">QR Code do Produto</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Criar o botão HTML centralizado
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-top: 20px;">
                        <a href="data:image/png;base64,{qr_code_base64}" 
                        download="qrcode.png"
                        style="
                                display: inline-block;
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px 20px;
                                text-align: center;
                                text-decoration: none;
                                font-size: 16px;
                                border-radius: 8px;
                                border: none;
                        ">
                            ⬇️ Baixar QR Code
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error(message)

elif selected_tab == "Autenticação":
    st.header("Autenticar com Qr Code")
    
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
                    is_match, matching_block = verify_product(auth_image, auth_person_id)
                    
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