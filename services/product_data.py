import json

class ProductData:
    def __init__(self,
                 product_id,
                 product_name,
                 batch_number,
                 manufacture_date,
                 manufacturer,
                 manufacturing_location,
                 brief_description,
                 capture_date):
            """
            Inicializa os dados do produto
            ::param product_id: Numero identificador do produto
            :param product_name: Nome do produto
            :param batch_number: Número do lote
            :param manufacture_date: Data de fabricação
            :param manufacturer: Fabricante
            :param manufacturing_location: Local de fabricação
            :param brief_description: Breve descrição do produto
            :param capture_date: Data de registro na blockchain
            """
            self.product_id = product_id
            self.product_name = product_name
            self.batch_number = batch_number
            self.manufacture_date = manufacture_date
            self.manufacturer = manufacturer
            self.manufacturing_location = manufacturing_location
            self.brief_description = brief_description
            self.capture_date = capture_date
    
    def to_json(self):
        """
        Converte os dados para JSON
        """
        data = {
            "product_id" : self.product_id,
            "product_name" : self.product_name,
            "batch_number" : self.batch_number,
            "manufacture_date" : self.manufacture_date,
            "manufacturer" : self.manufacturer,
            "manufacturing_location" : self.manufacturing_location,
            "brief_description" : self.brief_description,
            "capture_date" : self.capture_date
        }
        return json.dumps(data)
    
    @staticmethod
    def from_json(json_str):
        """
        Cria uma instância de ProductData a partir de uma string JSON
        """
        data = json.loads(json_str)
        return ProductData(
                        data["product_id"],
                        data["product_name"],
                        data["batch_number"],
                        data["manufacture_date"], 
                        data["manufacturer"],
                        data["manufacturing_location"],
                        data["brief_description"],
                        data["capture_date"])

    def to_dict(self):
        data ={
            'product_id': self.product_id,
            'product_name': self.product_name,
            'batch_number': self.batch_number,
            'manufacture_date': self.manufacture_date,
            'manufacturer': self.manufacturer,
            'manufacturing_location': self.manufacturing_location,
            'brief_description': self.brief_description,
            'capture_date': self.capture_date
        }
        return(data)
    
    