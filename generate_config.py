import os
from dotenv import load_dotenv
import json

def generate_config():
    """Genera un archivo de configuración portable"""
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener configuraciones necesarias
    config = {
        'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
        'MONGODB_URI': os.getenv('MONGODB_URI'),
        'DATABASE_NAME': 'final_project',
        'PYTHON_VERSION': sys.version[:5],
        'NODE_VERSION': os.getenv('NODE_VERSION', '16.x'),
        'MONGODB_VERSION': os.getenv('MONGODB_VERSION', '6.x')
    }
    
    # Guardar configuración en un archivo JSON
    with open('project_config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print("\n=== Configuración generada ===")
    print(f"JWT_SECRET_KEY: {config['JWT_SECRET_KEY'][:10]}...")
    print(f"MONGODB_URI: {config['MONGODB_URI']}")
    print("\nEste archivo 'project_config.json' debe incluirse en el .zip")
    print("Para usarlo en otro computador, ejecuta 'setup.py' y luego:")
    print("1. Copiar el contenido de 'project_config.json'")
    print("2. Crear un nuevo archivo .env en el otro computador")
    print("3. Pegar el contenido en el nuevo archivo .env")

if __name__ == '__main__':
    generate_config()
