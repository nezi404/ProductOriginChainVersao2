# blockchain.py
# Classe que representa a Blockchain
import json
from services.product_data import ProductData
from services.block_class import Block
import time
from pathlib import Path

class Blockchain:
    def __init__(self, difficulty, file_path="blockchain.json"):
        """
        Inicializa a blockchain com um bloco gênesis
        :param difficulty: Dificuldade da mineração (número de zeros iniciais exigidos no hash)
        """
        self.difficulty = difficulty
        self.blocks = []
        self.file_path = Path(file_path)
        self.load_or_create()
        
        
    
    def create_genesis_block(self):
        """
        Cria o primeiro bloco da blockchain (Bloco Gênesis)
        """
        genesis_block = Block(0, time.time(), None, "Block gênesis")
        genesis_block.proof_of_work(self.difficulty)
        self.blocks.append(genesis_block)
        self.save()
    
    def latest_block(self):
        """
        Retorna o último bloco da blockchain
        """
        return self.blocks[-1]
    
    def new_block(self, data):
        """
        Cria um novo bloco baseado no último bloco da blockchain
        :param data: Dados que serão armazenados no bloco
        """
        latest_block = self.latest_block()
        print("Novo bloco", data.product_name)
        print("Novo bloco eeeee", data.to_dict())
        print("Novo bloco", type(data))
        return Block(latest_block.index + 1, time.time(), latest_block.hash, data)    
       
   
    def add_block(self, block):
        """
        Adiciona um novo bloco à blockchain após validar sua Proof-of-Work
        """
        if block and self.is_valid_new_block(block, self.latest_block()):
            block.proof_of_work(self.difficulty)
            self.blocks.append(block)
            self.save()

    
    def is_first_block_valid(self):
        """
        Verifica se o bloco gênesis é válido
        """
        first_block = self.blocks[0]
        return (first_block.index == 0 and
                first_block.previous_hash is None and
                first_block.hash == first_block.calculate_hash())
    
    def is_valid_new_block(self, new_block, previous_block):
        """
        Valida um novo bloco com base no bloco anterior
        """
        return (new_block and previous_block and
                previous_block.index + 1 == new_block.index and
                new_block.previous_hash == previous_block.hash and
                new_block.hash == new_block.calculate_hash())
    
    def is_blockchain_valid(self):
        """
        Verifica a integridade da blockchain
        """
        if not self.is_first_block_valid():
            return False
        
        #//Percorre todos os blocos da blockchain
        #//verifica cada bloco em relação ao seu antecessor.
        #//Isso confirma que a blockchain inteira não foi adulterada.
        for i in range(1, len(self.blocks)):
            if not self.is_valid_new_block(self.blocks[i], self.blocks[i-1]):
                return False
        
        return True
    
    def find_block(self, b):
        
        if  len(self.blocks) == 1:
            print("Nenhum produto registrado")
            return False, False

        for i in range(1, len(self.blocks)):
    
            if b['product_id'] == self.blocks[i].data.product_id  and b['product_name'] == self.blocks[i].data.product_name and b['batch_number'] == self.blocks[i].data.batch_number: 
                print("produto achado")
                return True, self.blocks[i]
            else:
                print("produto nao achado")
        
        return False, False
    
    def __str__(self):
        """
        Retorna a representação textual de toda a blockchain
        """
        return '\n'.join(str(block) for block in self.blocks)
    
    def save_block(self, block):
        b = json.dumps(block.to_dict())
        # Writing to blockchain.json
        with open("blockchain.json", "a") as outfile:
            outfile.write(b)
    
    def save(self):
        with self.file_path.open('w') as f:
            print("é na hora de salvarrrr")
            json.dump([block.to_dict() for block in self.blocks], f, indent=2)

    def load_or_create(self):
        if self.file_path.exists():
            with self.file_path.open() as f:
                data = json.load(f)
                self.blocks = [Block.from_dict(b) for b in data]
        else:
            self.create_genesis_block()


        