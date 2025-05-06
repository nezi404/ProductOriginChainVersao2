# block.py
# Classe que representa um bloco individual na blockchain
import hashlib
import time
import json
from services.product_data import ProductData

class Block:
    def __init__(self, index, timestamp, previous_hash, data, nonce=0):
        """
        Inicializa um bloco com os atributos necessários
        :param index: Índice do bloco na blockchain
        :param timestamp: Timestamp de criação do bloco
        :param previous_hash: Hash do bloco anterior
        :param data: Dados armazenados no bloco (pode ser string ou ProductData)
        """
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calcula o hash do bloco utilizando SHA-256
        """
        # Converte os dados para string JSON se for ProductData
        if isinstance(self.data, ProductData):
            data_str = self.data.to_json()
        else:
            data_str = str(self.data)
            
        data_str = f"{self.index}{self.timestamp}{self.previous_hash}{data_str}{self.nonce}"
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def proof_of_work(self, difficulty):
        """
        Implementa o algoritmo de Proof-of-Work para validar o bloco
        :param difficulty: Nível de dificuldade definido para a blockchain
        """
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        print("funcao dict aaa", self.data)
        if self.previous_hash == None:
            print("igual none")
            return  {
                "index": self.index,
                "timestamp": self.timestamp,
                "previous_hash": self.previous_hash,
                "Data": self.data,
                "nonce": self.nonce,
                "hash": self.hash
            }
        else:
            print("funcao dict aaa", self.data.to_dict())

            return {
                "index": self.index,
                "timestamp": self.timestamp,
                "previous_hash": self.previous_hash,
                "Data": self.data.to_dict(),
                "nonce": self.nonce,
                "hash": self.hash
            }
    
    @staticmethod
    def from_dict(data):
        print("ABAXACI")
        print(data)
        prod_data = data
        
        if prod_data["index"] > 0:
            print("nao é o bloco genesisi")
            print(prod_data["Data"])
        
            prod = ProductData(
                            prod_data["Data"]["product_id"],
                            prod_data["Data"]["product_name"],
                            prod_data["Data"]["batch_number"],
                            prod_data["Data"]["manufacture_date"], 
                            prod_data["Data"]["manufacturer"],
                            prod_data["Data"]["manufacturing_location"],
                            prod_data["Data"]["brief_description"],
                            prod_data["Data"]["capture_date"])
            return Block(data["index"], data["timestamp"], data["previous_hash"],prod, data["nonce"])
        else:
            return Block(data["index"], data["timestamp"], data["previous_hash"], None, data["nonce"])
            
    def to_json(self):
        print("funcao jsonnn", self.data)
        print("o index é", self.index)
        if self.index != 0:
            print("funcao jsonnn comdata", self.data)
            data =  {
                "index": self.index,
                "timestamp": self.timestamp,
                "previous_hash": self.previous_hash,
                "data": self.data.to_dict(),
                "nonce": self.nonce,
                "hash": self.hash
            }
        else:
            data = {
                "index": self.index,
                "timestamp": self.timestamp,
                "previous_hash": self.previous_hash,
                "data": self.data,
                "nonce": self.nonce,
                "hash": self.hash
            }
        return json.dumps(data)
    
    def __str__(self):
        """
        Retorna a representação textual do bloco
        """
        data_str = self.data.to_json() if isinstance(self.data, ProductData) else str(self.data)
        return f"Block #{self.index} [previousHash: {self.previous_hash}, timestamp: {time.ctime(self.timestamp)}, data: {data_str}, hash: {self.hash}]"
