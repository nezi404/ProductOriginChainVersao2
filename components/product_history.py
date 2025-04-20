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
                    **Hash:** `{block.hash}`  
                    **Dados:** {block.data}
                    """)
                    st.markdown("---")