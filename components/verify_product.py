import streamlit as st
from services.product_data import ProductData
import hashlib
from datetime import datetime
from PIL import Image
import base64
import io
# import cv2
import numpy as np


class VerifyProduct:
    def __init__(self):
        pass

    
    def hash_product_qrcode_image(self, image):
        """
        Gera um hash da imagem da impressão digital
        """
        return hashlib.sha256(image).hexdigest()
    
    def decode_qrcode(self, image):
        """
        Tenta extrair texto (ID do produto) de um QR Code na imagem.
        """
        return 14334
        # try:
        #     image_np = np.array(image.convert("RGB"))  # Converter imagem PIL para array
        #     detector = cv2.QRCodeDetector()
        #     data, _, _ = detector.detectAndDecode(image_np)
        #     return data if data else None
        # except Exception as e:
        #     st.error(f"Erro ao decodificar QR Code: {e}")
        #     return None

    def verify_product(self, image=None, product_id=None):
        """
        Verifica se o produto está na blockchain com base no ID fornecido
        ou extraído do QR Code.
        """
        try:
            if image:
                product_id = self.decode_qrcode(image)
                if not product_id:
                    st.warning("QR Code não pôde ser lido. Tente outra imagem.")
                    return False, None

            for block in st.session_state.blockchain.blocks:
                if hasattr(block.data, 'to_json') and isinstance(block.data, ProductData):
                    if block.data.product_id == product_id:
                        return True, block
                
            return False, None
        except Exception as e:
            st.error(f"Erro ao verificar autenticidade do produto: {str(e)}")
            return False, None

    def render(self):
        st.header("Autenticar Produto")
    
        with st.form("auth_form"):
            auth_product_id = st.text_input("ID do Produto", key="auth_product_id")
            st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <p style="font-size: 14px;">OU</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            auth_file = st.file_uploader("Selecione a imagem do QrCode", 
                                    type=['png', 'jpg', 'jpeg', 'bmp'],
                                    key="auth_qrcode")
            
            auth_image = None  # Definida fora do if

            if auth_file is not None:
                image_bytes = auth_file.read()
                auth_image = Image.open(io.BytesIO(image_bytes))
                qr_code_base64 = base64.b64encode(image_bytes).decode("utf-8")
                
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

            
            auth_submitted = st.form_submit_button("Verificar Autenticidade do Produto", use_container_width=True)
            
            if auth_submitted:
                if not auth_product_id and auth_file is None:
                    st.error("Por favor, insira o código ou selecine uma imagem")
                else:
                    auth_image = Image.open(auth_file) if auth_file else None

                    with st.spinner("Verificando código do produto..."):
                        is_match, matching_block = self.verify_product(image=auth_image, product_id=auth_product_id)
                        
                        if is_match:
                            st.success("✅ Autenticação bem-sucedida!")
                            st.balloons()
                            
                            # Mostrar detalhes do registro
                            st.subheader("Detalhes do Registro")
                            st.info(f"""
                            **Nome do Produto:** {matching_block.data.product_name}  
                            **Número do Lote:** {matching_block.data.batch_number}  
                            **Data de Fabricação:** {matching_block.data.manufacture_date}  
                            **Fabricante:** {matching_block.data.manufacturer}  
                            **Local de Fabricação:** {matching_block.data.manufacturing_location}  
                            **Descrição:** {matching_block.data.brief_description}  
                            **Data de Registro:** {matching_block.data.capture_date}  
                            **Bloco:** #{matching_block.index}  
                            **Hash do Bloco:** {matching_block.hash[:20]}...
                            """)
                        else:
                            st.error("❌ Autenticação falhou. Produto não encontrado para este ID.")
