from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
import os
import requests
from bs4 import BeautifulSoup
from models import init_mongo, User, Article, mongo

# Configuración inicial
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["*"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization", "Accept"], "expose_headers": ["Authorization"]}})
load_dotenv()

# Configuración de MongoDB
app.config['MONGO_URI'] = os.getenv('MONGODB_URI_PROD') if os.getenv('FLASK_ENV') == 'production' else os.getenv('MONGODB_URI', 'mongodb://localhost:27017/final_project')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY_PROD') if os.getenv('FLASK_ENV') == 'production' else os.getenv('JWT_SECRET_KEY', 'your-secret-key')

# Inicializar MongoDB y JWT
init_mongo(app)
jwt = JWTManager(app)

# Configuración de Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sistema de Gestión de Contenidos",
        'deepLinking': True,
        'displayOperationId': True,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'options'],
        'displayRequestDuration': True,
        'docExpansion': 'list',
        'persistAuthorization': True,
        'showRequestHeaders': True,
        'showCommonExtensions': True
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)



# Función para procesar texto
def process_text(text):
    # Simplemente convertir a minúsculas y dividir por espacios
    return ' '.join(text.lower().split())

# Rutas de autenticación
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'password', 'email']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    if User.find_by_username(data['username']):
        return jsonify({'error': 'Usuario ya existe'}), 400
    
    User.create(data['username'], data['password'], data['email'])
    return jsonify({'message': 'Usuario registrado'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_username(data['username'])
    if user and user['password'] == data['password']:  # En producción usar bcrypt
        access_token = create_access_token(identity=user['username'], expires_delta=timedelta(hours=1))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Credenciales inválidas'}), 401

# Ruta de prueba para verificar la conexión a MongoDB
@app.route('/api/test', methods=['GET'])
def test_db():
    try:
        # Intentar una operación simple para verificar la conexión
        mongo.db.command('ping')
        return jsonify({
            'message': 'Conexión a MongoDB exitosa',
            'collections': list(mongo.db.list_collection_names())
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta de prueba para crear un usuario de prueba
@app.route('/api/test/create-user', methods=['POST'])
def create_test_user():
    try:
        # Crear un usuario de prueba
        User.create(
            username='test_user',
            password='test_password',
            email='test@example.com'
        )
        return jsonify({'message': 'Usuario de prueba creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas protegidas
@app.route('/api/articles', methods=['GET'])
@jwt_required()
def get_articles():
    articles = list(mongo.db.articles.find({}, {'_id': 0}))
    return jsonify(articles)

@app.route('/api/articles', methods=['POST'])
@jwt_required()
def add_article():
    data = request.get_json()
    processed_content = process_text(data['content'])
    article = {
        'title': data['title'],
        'content': data['content'],
        'processed_content': processed_content,
        'created_at': datetime.utcnow()
    }
    mongo.db.articles.insert_one(article)
    return jsonify({'message': 'Artículo agregado'}), 201

@app.route('/api/scrape', methods=['POST'])
@jwt_required()
def scrape_website():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL requerida'}), 400
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer contenido relevante
        content = ''
        for p in soup.find_all('p'):
            content += p.get_text() + ' '
        
        # Procesar y guardar el contenido
        processed_content = process_text(content)
        article = {
            'url': url,
            'content': content,
            'processed_content': processed_content,
            'created_at': datetime.utcnow()
        }
        mongo.db.articles.insert_one(article)
        return jsonify({'message': 'Contenido extraído y procesado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    data = request.get_json()
    user_preferences = data.get('user_preferences')
    if not user_preferences:
        return jsonify({'error': 'Preferencias del usuario requeridas'}), 400
    
    # Obtener todos los artículos
    articles = list(mongo.db.articles.find())
    
    # Filtrar artículos que contengan palabras clave de las preferencias del usuario
    recommended_articles = []
    user_keywords = user_preferences.lower().split()
    
    for article in articles:
        article_text = article['content'].lower()
        if any(keyword in article_text for keyword in user_keywords):
            recommended_articles.append({
                'title': article['title'],
                'content': article['content'],
                'url': article['url']
            })
    
    return jsonify(recommended_articles[:5]), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
