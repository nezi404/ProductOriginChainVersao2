import streamlit as st
from datetime import datetime


class ProductsHistory:
    def __init__(self):
        pass

    def render(self):
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
                    **Hash:** `{block.hash}
                    """)

                    if block.index == 0:
                        # st.info("🧱 Este é o bloco gênesis da blockchain.")
                        st.markdown(f"**Dados:** {block.data}")
                    else:
                        # Verifica o tipo dos dados
                        if isinstance(block.data, dict):
                            data = block.data
                        elif hasattr(block.data, "to_dict"):
                            data = block.data.to_dict()
                        else:
                            data = {"mensagem": str(block.data)}

                        st.markdown(f"""
                        **Dados:**                     
                        **Nome do Produto:** {data.get("product_name", "N/A")}  
                        **Número do Lote:** {data.get("batch_number", "N/A")}  
                        **Data de Fabricação:** {data.get("manufacture_date", "N/A")}  
                        **Fabricante:** {data.get("manufacturer", "N/A")}  
                        **Local de Fabricação:** {data.get("manufacturing_location", "N/A")}  
                        **Descrição:** {data.get("brief_description", "N/A")}  
                        **Data de Registro:** {data.get("capture_date", "N/A")}  
                        """)

                    st.markdown("-------------")