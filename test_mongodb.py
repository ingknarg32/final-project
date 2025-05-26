from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URI de MongoDB desde el archivo .env
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/final_project')

try:
    # Intentar conectar a MongoDB
    client = MongoClient(mongo_uri)
    # Intentar una operación simple para verificar la conexión
    client.admin.command('ping')
    print("¡Conexión exitosa a MongoDB!")
    
    # Listar las bases de datos disponibles
    print("\nBases de datos disponibles:")
    print(client.list_database_names())
    
    # Crear una base de datos de prueba
    db = client['test_db']
    print("\nBase de datos 'test_db' creada")
    
    # Crear una colección de prueba
    collection = db['test_collection']
    print("Colección 'test_collection' creada")
    
    # Insertar un documento de prueba
    test_document = {
        'nombre': 'Prueba',
        'timestamp': datetime.now()
    }
    result = collection.insert_one(test_document)
    print(f"\nDocumento insertado con ID: {result.inserted_id}")
    
    # Leer el documento
    print("\nDocumento leído:")
    print(collection.find_one({'nombre': 'Prueba'}))
    
except Exception as e:
    print(f"Error al conectar a MongoDB: {str(e)}")
