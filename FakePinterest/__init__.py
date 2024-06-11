# Importa as classes e funções necessárias do Flask e suas extensões
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Cria uma instância do Flask
app = Flask(__name__)

# Configura a URI do banco de dados SQLite que será usado pela aplicação
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
# Configura a chave secreta da aplicação, usada para segurança (sessões, CSRF, etc.)
app.config["SECRET_KEY"] = "S&nh@PR@t&GID@_06892882942706_pR@t&gId@-S&nh@"
# Configura o diretório onde as fotos dos posts serão armazenadas
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

# Cria uma instância do SQLAlchemy, que gerencia a interação com o banco de dados
database = SQLAlchemy(app)
# Cria uma instância do Bcrypt, usada para hashing de senhas
bcrypt = Bcrypt(app)
# Cria uma instância do LoginManager, que gerencia a autenticação de usuários
login_manager = LoginManager(app)
# Define a visão de login padrão, usada pelo LoginManager para redirecionar usuários não autenticados
login_manager.login_view = "homepage"

# Importa as rotas definidas no módulo routes do FakePinterest após a criação da instância app
# Isso é feito para evitar importações circulares, onde os módulos dependem uns dos outros
from FakePinterest import routes
