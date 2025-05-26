import os
import sys
import subprocess
import nltk
from dotenv import load_dotenv
import platform
import shutil
import json

print("\n=== Iniciando instalación del proyecto ===\n")

# Verificar sistema operativo
print(f"Sistema operativo: {platform.system()}")

# 1. Verificar Python
print("\n1. Verificando Python...")
try:
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 o superior es requerido")
        sys.exit(1)
    print(f"✅ Python {python_version.major}.{python_version.minor} encontrado")
except Exception as e:
    print(f"❌ Error al verificar Python: {str(e)}")
    sys.exit(1)

# 2. Instalar dependencias de Python
print("\n2. Instalando dependencias de Python...")
try:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    print("✅ Dependencias de Python instaladas exitosamente")
except subprocess.CalledProcessError as e:
    print(f"❌ Error al instalar dependencias de Python: {str(e)}")
    sys.exit(1)

# 3. Descargar recursos de NLTK
print("\n3. Descargando recursos de NLTK...")
try:
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    print("✅ Recursos de NLTK descargados exitosamente")
except Exception as e:
    print(f"❌ Error al descargar recursos de NLTK: {str(e)}")
    sys.exit(1)

# 4. Verificar Node.js
print("\n4. Verificando Node.js...")
try:
    subprocess.run(['node', '--version'], check=True, capture_output=True)
    print("✅ Node.js encontrado")
except subprocess.CalledProcessError:
    print("❌ Node.js no encontrado. Por favor, instálalo desde: https://nodejs.org/")
    sys.exit(1)

# 5. Verificar MongoDB
print("\n5. Verificando MongoDB...")
try:
    # Intentar conectar a MongoDB
    from pymongo import MongoClient
    
    # Verificar si existe archivo de configuración
    if os.path.exists('project_config.json'):
        with open('project_config.json', 'r') as f:
            config = json.load(f)
            mongo_uri = config.get('MONGODB_URI', 'mongodb://localhost:27017/final_project')
    else:
        mongo_uri = 'mongodb://localhost:27017/final_project'
    
    client = MongoClient(mongo_uri)
    client.admin.command('ping')
    print("✅ MongoDB está funcionando correctamente")
except Exception as e:
    print(f"❌ Error al conectar a MongoDB: {str(e)}")
    print("\nPor favor, asegúrate de que:")
    print("1. MongoDB está instalado en tu sistema")
    print("2. El servicio de MongoDB está en ejecución")
    print("3. La URL de MongoDB en el archivo .env es correcta")
    sys.exit(1)

# 6. Configurar archivo .env
print("\n6. Configurando archivo .env...")
if not os.path.exists('.env'):
    try:
        if os.path.exists('project_config.json'):
            with open('project_config.json', 'r') as f:
                config = json.load(f)
                env_content = f"""
JWT_SECRET_KEY={config['JWT_SECRET_KEY']}
MONGODB_URI={config['MONGODB_URI']}
FLASK_APP=app.py
FLASK_ENV=development
"""
            with open('.env', 'w') as env_file:
                env_file.write(env_content)
            print("✅ Archivo .env creado usando configuración portable")
        else:
            shutil.copy('.env.example', '.env')
            print("✅ Archivo .env creado usando ejemplo")
    except Exception as e:
        print(f"❌ Error al crear archivo .env: {str(e)}")
        sys.exit(1)

# 7. Iniciar el servidor
print("\n=== Todo listo! Iniciando el servidor ===\n")

# Iniciar el servidor Flask
try:
    subprocess.Popen([sys.executable, 'app.py'])
    print("✅ Servidor Flask iniciado")
except Exception as e:
    print(f"❌ Error al iniciar el servidor: {str(e)}")
    sys.exit(1)

print("\n=== Instrucciones ===")
print("1. El servidor Flask está corriendo en http://localhost:5000")
print("2. Para iniciar el frontend:")
print("   - Navega a la carpeta 'client'")
print("   - Ejecuta 'npm install'")
print("   - Ejecuta 'npm start'")
print("\n¡Listo! Puedes empezar a usar la aplicación.")
print("\nSi encuentras algún error, por favor revisa el README.md para más detalles.")
print("\nNota: Si el proyecto no funciona correctamente, verifica que:")
print("1. Los servicios de MongoDB estén en ejecución")
print("2. Las versiones de Python, Node.js y MongoDB sean compatibles")
print("3. El archivo .env tenga las configuraciones correctas")
