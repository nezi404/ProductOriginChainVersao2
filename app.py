from flask import Flask, render_template, request, jsonify
from blockchain import Blockchain
from product_data import ProductData
import hashlib
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Criar diretório de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar a blockchain
blockchain = Blockchain(difficulty=4)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_fingerprint_image(image_data):
    """
    Gera um hash da imagem da impressão digital
    """
    return hashlib.sha256(image_data).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fingerprint' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['fingerprint']
    person_id = request.form.get('person_id', '')
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
    
    if not person_id:
        return jsonify({'error': 'ID da pessoa é obrigatório'}), 400
    
    try:
        # Ler os dados da imagem
        image_data = file.read()
        
        # Gerar hash da imagem
        fingerprint_hash = hash_fingerprint_image(image_data)
        
        # Criar dados biométricos
        biometric_data = ProductData(
            fingerprint_hash=fingerprint_hash,
            person_id=person_id,
            capture_date=datetime.now().isoformat(),
            quality_score=95  # Em um caso real, isso seria calculado baseado na qualidade da imagem
        )
        
        # Adicionar à blockchain
        new_block = blockchain.new_block(biometric_data)
        blockchain.add_block(new_block)
        
        return jsonify({
            'success': True,
            'message': 'Impressão digital registrada com sucesso',
            'block_index': new_block.index,
            'hash': new_block.hash
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/blockchain')
def get_blockchain():
    return jsonify({
        'blocks': [str(block) for block in blockchain.blocks],
        'is_valid': blockchain.is_blockchain_valid()
    })

if __name__ == '__main__':
    app.run(debug=True) 