# Importa o banco de dados SQLAlchemy e o gerenciador de login do Flask
from FakePinterest import database, login_manager
# Importa a classe datetime para manipulação de datas e horas
from datetime import datetime
# Importa UserMixin para facilitar a implementação de métodos necessários para o Flask-Login
from flask_login import UserMixin
# Define a função para carregar o usuário pelo ID, necessária para o Flask-Login
@login_manager.user_loader
def load_usuario(id_usuario):
    # Busca e retorna um usuário pelo ID no banco de dados
    return Usuario.query.get(int(id_usuario))
# Define o modelo de usuário, que representa os usuários no banco de dados
class Usuario(database.Model, UserMixin):
    # Define a coluna ID como chave primária e autoincrementada
    id = database.Column(database.Integer, primary_key=True)
    # Define a coluna nome como string, não pode ser nula
    nome = database.Column(database.String, nullable=False)
    # Define a coluna email como string, não pode ser nula e deve ser única
    email = database.Column(database.String, nullable=False, unique=True)
    # Define a coluna senha como string, não pode ser nula
    senha = database.Column(database.String, nullable=False)
    # Define o relacionamento um-para-muitos com o modelo Foto
    fotos = database.relationship("Foto", backref="usuario", lazy=True)

# Define o modelo de foto, que representa as fotos no banco de dados
class Foto(database.Model):
    # Define a coluna ID como chave primária e autoincrementada
    id = database.Column(database.Integer, primary_key=True)
    # Define a coluna images como string, com um valor padrão "default.png"
    images = database.Column(database.String, default="default.png")
    # Define a coluna data_criacao como DateTime, não pode ser nula, com valor padrão da data/hora atual
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    # Define a coluna id_usuario como integer, chave estrangeira referenciando a tabela usuario, não pode ser nula
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

