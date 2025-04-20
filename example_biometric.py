from blockchain import Blockchain
from product_data import ProductData
import hashlib
from datetime import datetime

def hash_fingerprint_image(image_data):
    """
    Gera um hash da imagem da impressão digital
    :param image_data: Dados binários da imagem
    :return: Hash SHA-256 da imagem
    """
    return hashlib.sha256(image_data).hexdigest()

def main():
    # Criar uma blockchain com dificuldade 4
    blockchain = Blockchain(difficulty=4)
    
    # Exemplo de dados de impressão digital (em um caso real, isso viria de um scanner)
    fingerprint_image_data = b"dados_binarios_da_imagem"  # Substitua pelos dados reais da imagem
    
    # Criar hash da impressão digital
    fingerprint_hash = hash_fingerprint_image(fingerprint_image_data)
    
    # Criar dados biométricos
    biometric_data = ProductData(
        fingerprint_hash=fingerprint_hash,
        person_id="P123456",
        capture_date=datetime.now().isoformat(),
        quality_score=95
    )
    
    # Criar e adicionar um novo bloco com os dados biométricos
    new_block = blockchain.new_block(biometric_data)
    blockchain.add_block(new_block)
    
    # Verificar se a blockchain é válida
    print("Blockchain válida:", blockchain.is_blockchain_valid())
    
    # Imprimir a blockchain
    print("\nBlockchain:")
    print(blockchain)

if __name__ == "__main__":
    main() 