# Proyecto Final de Desarrollo Web

## Descripción
Este proyecto es un blog interactivo que permite a los usuarios crear cuentas, publicar artículos y explorar contenido interesante a través de web scraping.

# Sistema de Gestión de Contenidos

Sistema web completo para gestión de contenidos con funcionalidades de autenticación, procesamiento de texto y web scraping.

## 🚀 Instalación

### 1. Requisitos Previos

Antes de comenzar, asegúrate de tener instalados:

- Python 3.8 o superior
- Node.js 16 o superior
- MongoDB

### 2. Instalación de Dependencias

1. Clona el repositorio:
```bash
git clone [URL_DEL_REPO]
cd final-project
```

2. Instala las dependencias de Python:
```bash
pip install -r requirements.txt
```

3. Instala las dependencias del frontend:
```bash
cd client
npm install
```

### 3. Configuración del Entorno

1. Crea un archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```

2. Edita el archivo `.env` y configura:
- JWT_SECRET_KEY: Clave secreta para JWT
- MONGODB_URI: URL de conexión a MongoDB

### 4. Iniciar el Servidor

1. Iniciar el servidor backend:
```bash
python app.py
```

2. En otra terminal, iniciar el frontend:
```bash
cd client
npm start
```

## 🛠️ Estructura del Proyecto

```
final-project/
├── client/              # Frontend React
│   ├── public/
│   └── src/
│       ├── components/
│       └── App.js
├── app.py              # Backend Flask
├── models.py           # Modelos MongoDB
├── requirements.txt    # Dependencias Python
├── .env                # Variables de entorno
└── README.md          # Documentación
```

## 📱 Funcionalidades

- 🚀 Sistema de autenticación JWT
- 📝 Gestión de artículos
- 🕸️ Web scraping
- 📊 Procesamiento de texto
- 📱 Diseño responsive
- 🔐 Seguridad implementada

## 🔒 Seguridad

- Autenticación JWT
- Validación de entradas
- Protección contra XSS
- Protección contra CSRF
- CORS configurado

## 📊 Documentación de API

La documentación de la API está disponible en:

http://localhost:5000/api/docs

## 📈 Despliegue

El proyecto está listo para ser desplegado en:
- Vercel (Frontend)
- Railway (Backend)
- MongoDB Atlas (Base de datos)

## 🤝 Contribución

¡Contribuciones son bienvenidas! Por favor crea un Pull Request.

## Seguridad

- Autenticación JWT
- Validación de entradas
- Protección CORS
- Manejo seguro de contraseñas

## Optimización

- SEO optimizado
- Carga rápida
- Diseño responsive
- Buenas prácticas de desarrollo

## Pruebas

El proyecto incluye pruebas unitarias y de integración.

## Despliegue

El proyecto está listo para desplegarse en plataformas como:
- Vercel (Frontend)
- Railway (Backend)
- MongoDB Atlas (Base de datos)

## Contribución

¡Contribuciones son bienvenidas! Por favor crea un Pull Request.

## Estado del Proyecto

En desarrollo activo. Para contribuir, por favor crea un issue o pull request.
