# main.py
# Arquivo principal para executar a blockchain
from blockchain import Blockchain

def main():
    """
    Função principal para inicializar e testar a blockchain
    """
    blockchain = Blockchain(4)
    
    blockchain.add_block(blockchain.new_block("Tout sur le Bitcoin"))
    blockchain.add_block(blockchain.new_block("Sylvain Saurel"))
    blockchain.add_block(blockchain.new_block("https://www.toutsurlebitcoin.fr"))
    blockchain.add_block(blockchain.new_block("https://www.uea.edu.br"))
    
    print(blockchain)
    
    # Verifica se a blockchain é válida
    print("Blockchain é válida?", "Sim" if blockchain.is_blockchain_valid() else "Não")

if __name__ == "__main__":
    main()