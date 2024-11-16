from flask import Flask, jsonify
from flask_cors import CORS  # Importando CORS
import pandas as pd
import os

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)  # Permite todas as origens por padrão

# Função para criar o arquivo Excel com dados padrão, caso não exista
def create_excel_file():
    if not os.path.exists('sales.xlsx'):
        data = {
            'id': [1, 2, 3],
            'descricao': ['Produto A', 'Produto B', 'Produto C'],
            'valor': [10.0, 20.0, 30.0]
        }
        df = pd.DataFrame(data)
        df.to_excel('sales.xlsx', index=False)
        print("Arquivo sales.xlsx criado com dados padrão.")

# Função para ler o arquivo Excel
def read_excel():
    df = pd.read_excel('sales.xlsx')
    return df

# Rota para verificar todos os produtos
@app.route('/api/produtos', methods=['GET'])
def get_all_products():
    create_excel_file()  # Certifica-se de que o arquivo existe
    df = read_excel()
    products = df[['id', 'descricao', 'valor']].to_dict(orient='records')
    return jsonify(products)

# Rota para verificar um produto através do ID
@app.route('/api/produto/<int:id>', methods=['GET'])
def get_product_by_id(id):
    create_excel_file()  # Certifica-se de que o arquivo existe
    df = read_excel()
    product = df[df['id'] == id]
    if not product.empty:
        product_data = product[['id', 'descricao', 'valor']].iloc[0].to_dict()
        return jsonify(product_data)
    else:
        return jsonify({"error": "Produto não encontrado"}), 404

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
