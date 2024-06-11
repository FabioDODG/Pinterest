# Importa a instância da aplicação Flask do pacote FakePinterest
from FakePinterest import app

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    # Executa a aplicação Flask em modo de depuração (debug)
    app.run(debug=True)
