import json
import os
import streamlit as st
from components.register_product import RegisterProduct
from components.verify_product import VerifyProduct
from components.product_history import ProductsHistory
from components.sidebar import Sidebar
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
from web3 import Web3
load_dotenv()
class App:

    def run():
        # Configuração da página
        st.set_page_config(
            page_title="Blockchain de autenticidade de produtos eletrônicos",
            page_icon="🔒",
            layout="wide"
        )

        # Inicialização da blockchain (usando session_state para persistir entre reruns)
        if 'contract' not in st.session_state:
            # Carrega variáveis do .env
            
            st.private_key = os.getenv("PRIVATE_KEY")

            # Conexão Sepolia (Infura, Alchemy, etc.)
            st.provider_url = os.getenv("PROVIDER_URL")
            st.w3 = Web3(Web3.HTTPProvider(st.provider_url))
            st.account = st.w3.eth.account.from_key(st.private_key)
            st.sender_address = st.account.address

            # Endereço do contrato ProductsOriginChain
            st.contract_address = os.getenv("CONTRACT_ADDRESS")
            st.abi = '''
[
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "bool",
				"name": "exists",
				"type": "bool"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "product_id",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "product_name",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "batch_number",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "product_chain_id",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "manufacture_date",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "manufacturer",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "manufacturing_location",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "brief_description",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "capture_date",
				"type": "string"
			}
		],
		"name": "ProductRegistered",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "messsage",
				"type": "string"
			}
		],
		"name": "Test",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_product_chain_id",
				"type": "string"
			}
		],
		"name": "getProduct",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_product_id",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_product_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_batch_number",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_product_chain_id",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_manufacture_date",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_manufacturer",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_manufacturing_location",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_brief_description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_capture_date",
				"type": "string"
			}
		],
		"name": "register",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]                    
'''

            st.session_state.contract = st.contract = st.w3.eth.contract(address=st.contract_address, abi=json.loads(st.abi))

        # Estado para controlar qual aba está ativa
        if 'tab' not in st.session_state:
            st.session_state.tab = "registro"

        # Título principal
        st.title("🔒 Blockchain de Autenticidade de Produtos")

        # Tabs para navegação
        tabs = ["Registro", "Autenticação"]
        selected_tab = st.radio("Selecione uma opção:", tabs, horizontal=True)

        if selected_tab == "Registro":
            register_page = RegisterProduct()
            register_page.render()

        elif selected_tab == "Autenticação":
            verify_page = VerifyProduct()
            verify_page.render()

        # Sidebar com informações adicionais
        with st.sidebar:
            sidebar = Sidebar()
            sidebar.render()

App.run()