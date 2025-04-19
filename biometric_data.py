import hashlib
import json
from datetime import datetime

class BiometricData:
    def __init__(self, fingerprint_hash, person_id, capture_date, quality_score):
        """
        Inicializa os dados biométricos
        :param fingerprint_hash: Hash da imagem da impressão digital
        :param person_id: Identificador único da pessoa
        :param capture_date: Data e hora da captura
        :param quality_score: Pontuação de qualidade da captura (0-100)
        """
        self.fingerprint_hash = fingerprint_hash
        self.person_id = person_id
        self.capture_date = capture_date
        self.quality_score = quality_score
    
    def to_json(self):
        """
        Converte os dados para JSON
        """
        return json.dumps({
            'fingerprint_hash': self.fingerprint_hash,
            'person_id': self.person_id,
            'capture_date': self.capture_date,
            'quality_score': self.quality_score
        })
    
    @staticmethod
    def from_json(json_str):
        """
        Cria uma instância de BiometricData a partir de uma string JSON
        """
        data = json.loads(json_str)
        return BiometricData(
            data['fingerprint_hash'],
            data['person_id'],
            data['capture_date'],
            data['quality_score']
        ) 