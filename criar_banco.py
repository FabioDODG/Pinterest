# Importa as instâncias de banco de dados e da aplicação Flask do pacote FakePinterest
from FakePinterest import database, app
# Importa os modelos de dados Usuario e Foto do pacote FakePinterest.models
from FakePinterest.models import Usuario, Foto

# Entra no contexto da aplicação Flask para poder acessar as configurações e extensões do Flask
with app.app_context():
    # Cria todas as tabelas no banco de dados que estão definidas nos modelos de dados
    database.create_all()
