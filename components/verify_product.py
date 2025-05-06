import ast
import streamlit as st
from services.product_data import ProductData
from PIL import Image
import base64
import io
#import qreader
# import cv2
import numpy as np
from pyzbar.pyzbar import decode

class VerifyProduct:
    def __init__(self):
        pass

    def __read_qrcode_content(self, img):
        
        # Use the detect_and_decode function to get the decoded QR data
        decoded_text = decode(img)
        print(decoded_text[0].data)
        inf = decoded_text[0].data.decode("utf-8")
        print("No qr code", decoded_text)
        return inf
    
    
    def __to_dict(self, data):
        """
        Converte os dados para dicionario
        """
        
        dict = ast.literal_eval(data)
        return dict
    
    def read_qrcode(self, img):
        
        try:
            qr_code_text = self.__read_qrcode_content(img)
            print(qr_code_text)
        
            qr_code_dict = self.__to_dict(qr_code_text)
            return qr_code_dict
        except Exception as e: 
            print(f"Imagem inválida:{e}")
            return False
        
    def verify_product(self, image=None, product_id=None,product_name=None, batch_number=None):
        """
        Verifica se o produto está na blockchain com base no ID fornecido
        ou extraído do QR Code.
        """
        try:
            if image:
                find = self.read_qrcode(image)
                exists, block = st.session_state.blockchain.find_block(find)

                if exists and block:
                    print("achado com sucesso")
                    return True, block
                
            if product_id and product_name and batch_number:
                find = {
                    "product_id": product_id,
                    "product_name": product_name,
                    "batch_number": batch_number
                }
                exists, block = st.session_state.blockchain.find_block(find)
                
                if exists and block:
                    print("achado com sucesso")
                    return True, block

            #for block in st.session_state.blockchain.blocks[1:]:
            #   if hasattr(block.data, 'to_json') and isinstance(block.data, ProductData):
            #       if block.data.product_id == product_id and block.data.product_name == product_name:
            #            print("Isso tbm funciona")
            #            return True, block
                    
                
            return False, None
        except Exception as e:
            st.error(f"Erro ao verificar autenticidade do produto: {str(e)}")
            return False, None

    def render(self):
        st.header("Autenticar Produto")
    
        with st.form("auth_form"):
            auth_product_id = st.text_input("ID do Produto", key="auth_product_id")
            auth_product_name = st.text_input("Nome do Produto", key="auth_product_name")
            auth_batch_number = st.text_input("Número do lote", key="auth_batch_number")
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
                if not auth_product_id and not auth_product_name and auth_batch_number and auth_file is None:
                    st.error("Por favor, insira o código ou selecine uma imagem")
                else:
                    auth_image = Image.open(auth_file) if auth_file else None

                    with st.spinner("Verificando código do produto..."):
                        is_match, matching_block = self.verify_product(image=auth_image, product_id=auth_product_id, product_name=auth_product_name, batch_number=auth_batch_number)
                        
                        if is_match:
                            st.success("✅ Autenticação bem-sucedida!")
                            print(matching_block.data)
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
