from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId

# Inicializar MongoDB
mongo = PyMongo()

def init_mongo(app):
    mongo.init_app(app)

# Modelo de Usuario
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.created_at = datetime.utcnow()

    @staticmethod
    def create(username, password, email):
        user = {
            'username': username,
            'password': password,
            'email': email,
            'created_at': datetime.utcnow()
        }
        return mongo.db.users.insert_one(user)

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({'username': username})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})

# Modelo de Artículo
class Article:
    def __init__(self, title, content, user_id, url=None):
        self.title = title
        self.content = content
        self.processed_content = None
        self.url = url
        self.user_id = user_id
        self.created_at = datetime.utcnow()

    @staticmethod
    def create(title, content, user_id, url=None):
        article = {
            'title': title,
            'content': content,
            'processed_content': None,
            'url': url,
            'user_id': user_id,
            'created_at': datetime.utcnow()
        }
        return mongo.db.articles.insert_one(article)

    @staticmethod
    def find_all():
        return mongo.db.articles.find()

    @staticmethod
    def find_by_id(article_id):
        return mongo.db.articles.find_one({'_id': ObjectId(article_id)})

    @staticmethod
    def update_processed_content(article_id, processed_content):
        return mongo.db.articles.update_one(
            {'_id': ObjectId(article_id)},
            {'$set': {'processed_content': processed_content}}
        )
