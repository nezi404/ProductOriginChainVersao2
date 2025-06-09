import json
import streamlit as st
from datetime import datetime
from PIL import Image
from web3 import Web3
import qrcode
import base64
import io
import uuid
from dotenv import load_dotenv
import os



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
        product_chain_id = product_id + product_name + batch_number
        """
        Processa os dados do produto e adiciona à blockchain
        """
        try:
            nonce = st.w3.eth.get_transaction_count(st.sender_address)
            # Acessa a função store do contrato inteligente e prepara uma chamada com o parâmetro num (o número que o usuário digitou).
            # Constrói a transação em formato de dicionário Python, com os dados necessários para enviá-la à rede Ethereum.
            tx = st.contract.functions.register(
                                            product_id,
                                            product_name,
                                            batch_number,
                                            product_chain_id,
                                            manufacture_date, 
                                            manufacturer,
                                            manufacturing_location,
                                            brief_description,
                                            capture_date).build_transaction({
                'chainId': 11155111,  # Sepolia
                'gas': 500000, #Quantidade máxima de gás que a transação pode consumir. Fixado em 200000 unidades, o que é mais do que suficiente para essa função simples.
                'gasPrice': st.w3.to_wei('10', 'gwei'), #Define o preço do gás a ser pago por unidade. Convertido de 10 gwei para wei (menor unidade do ETH) usando w3.to_wei(...).
                'nonce': nonce #Define o nonce, ou seja, o número de transações já enviadas pela conta. Garante que cada transação tenha um número único, necessário para ser aceita pela rede.
            })

            signed_tx = st.w3.eth.account.sign_transaction(tx, st.private_key)
            tx_hash = st.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            st.success(f"✅ Transação enviada com sucesso!\nHash: {tx_hash.hex()}")

            # Espera a transação ser minerada
            receipt = st.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(receipt.logs)
            # Lê os eventos emitidos na transação
            logs = st.contract.events.ProductRegistered().process_receipt(receipt)

            log2 = st.contract.events.Test().process_receipt(receipt)
            if log2:
                product_values = logs[0]['args']
                st.info(f"📡 Evento capturado: informações do produto armazenado foi  test`{product_values}`")
                return True, "Registro realizado!"
            if not log2:
                st.warning("⚠️ Nenhum evento TEst encontrado na transação.")
                return False, f"Erro ao processar produto"
        
            if logs:
                product_values = logs[0]['args']
                st.info(f"📡 Evento capturado: informações do produto armazenado foi `{product_values}`")
                return True, "Registro realizado!"
            else:
                st.warning("⚠️ Nenhum evento ProductRegistered encontrado na transação.")
                return False, f"Erro ao processar produto"
        except Exception as e:
            st.error(f"Erro ao enviar transação: {str(e)}")
            return False, f"Erro ao processar produto: {str(e)}"
       
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
                manufacture_date = str(st.date_input("Data de fabricação", key="manufacture_date", value=None, format="DD/MM/YYYY", max_value="today"))

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
            
                success, message = self.process_product(
                    str(product_id),
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