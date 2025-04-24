import json
import streamlit as st
from services.product_data import ProductData
from datetime import datetime
from PIL import Image
import qrcode
import base64
import io
import uuid

class RegisterProduct:
    def __init__(self):
        pass
    def process_product(self, product_id,
                        product_name,
                        batch_number,
                        manufacture_date, 
                        manufacturer,
                        manufacturing_location,
                        brief_description,
                        capture_date
                        ):
        """
        Processa os dados do produto e adiciona à blockchain
        """
        try:

            product_data = ProductData(
                product_id = product_id,
                product_name =  product_name,
                batch_number = batch_number,
                manufacture_date = manufacture_date, 
                manufacturer = manufacturer,
                manufacturing_location = manufacturing_location,
                brief_description = brief_description,
                capture_date=capture_date,
                
            )
            
            # Adicionar à blockchain
            new_block = st.session_state.blockchain.new_block(product_data)
            st.session_state.blockchain.add_block(new_block)
            
            return True, "Produto registrado com sucesso!", new_block
        except Exception as e:
            return False, f"Erro ao processar produto: {str(e)}", None

    def generate_qrcode(self, data_dict):
        self.product_id = data_dict["product_id"]
        self.product_name = data_dict["product_name"]
        self.batch_number = data_dict["batch_number"]
        data_str = json.dumps(data_dict, indent=2)
        qr = qrcode.make(data_str)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        buf.seek(0)
        return buf
    
    def render(self):
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
            
            submitted = st.form_submit_button("Registrar Produto", use_container_width=True)
    

        if submitted:
            if not all([product_name, batch_number, manufacture_date, manufacturer, manufacturing_location, brief_description]):
                st.error("Por favor, Preencha todos os campos")
            else:
                capture_date = datetime.now().isoformat()
                product_id = str(uuid.uuid4())[:16]  # gera um ID único de 8 caracteres
            
                success, message, block = self.process_product(
                    product_id,
                    product_name,
                    batch_number,
                    manufacture_date, 
                    manufacturer,
                    manufacturing_location,
                    brief_description,
                    capture_date
                    )
                if success:
                    st.success(message)
                    # st.info(f"Hash do bloco: {block.hash}")

                    qr_code_img = self.generate_qrcode({
                        "product_id": product_id,
                        "product_name": product_name,
                        "batch_number": batch_number                        
                    })
                    
                    st.markdown(
                        f"""
                        <div style="text-align: center;">
                            <p style="font-size: 20px;">Código de verificação do produto: <strong>{product_id}</strong></p>
                            <p style="font-size: 20px;">Nome de verificação do produto: <strong>{product_name}</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Converta a imagem para base64
                    qr_code_base64 = base64.b64encode(qr_code_img.read()).decode("utf-8")
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