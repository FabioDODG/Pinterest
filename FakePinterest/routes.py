# Importa várias funções e classes essenciais do Flask e outras bibliotecas
# Funções do Flask para renderizar templates HTML, gerar URLs, redirecionar e exibir mensagens flash
from flask import render_template, url_for, redirect, flash 
# Importa o objeto Flask, o banco de dados SQLAlchemy e a biblioteca Bcrypt para hashing de senhas
from FakePinterest import app, database, bcrypt  
# Funções do Flask-Login para gerenciamento de sessões de usuário
from flask_login import login_user, logout_user, login_required, current_user  
# Importa os formulários personalizados do Flask-WTF
from FakePinterest.forms import FormCriarConta, FormLogin, FormFoto  
# Importa os modelos de banco de dados para usuários e fotos
from FakePinterest.models import Usuario, Foto  
# Biblioteca padrão do Python para interagir com o sistema operacional
import os  
# Função para garantir que o nome do arquivo enviado é seguro
from werkzeug.utils import secure_filename  

# Define a rota para a página inicial
@app.route("/", methods=["GET", "POST"]) # Permite que a página inicial tanto exiba o formulário de login (GET) quanto processe os dados enviados pelo formulário (POST)
def homepage():
    formulario_login = FormLogin()  # Cria uma instância do formulário de login
    if formulario_login.validate_on_submit():  # Verifica se o formulário foi enviado e é válido
        usuario = Usuario.query.filter_by(email=formulario_login.email.data).first()  # Busca um usuário no banco de dados pelo email fornecido
        if usuario and bcrypt.check_password_hash(usuario.senha, formulario_login.senha.data):  # Verifica se o usuário existe e se a senha está correta
            login_user(usuario)  # Faz o login do usuário
            return redirect(url_for("perfil", id_usuario=usuario.id))  # Redireciona para a página de perfil do usuário
    return render_template("homepage.html", form=formulario_login)  # Renderiza o template da homepage com o formulário de login

# Define a rota para a página de criação de conta
@app.route("/criar_conta", methods=["GET", "POST"]) # Permite que a página criar conta tanto exiba o formulário de login (GET) quanto processe os dados enviados pelo formulário (POST)
def criarconta():
    formulario_criar_conta = FormCriarConta()  # Cria uma instância do formulário de criação de conta
    if formulario_criar_conta.validate_on_submit():  # Verifica se o formulário foi enviado e é válido
        print("Dados do formulário:", formulario_criar_conta.email.data, formulario_criar_conta.nome.data, formulario_criar_conta.senha.data)  # Imprime os dados do formulário no console
        senha = bcrypt.generate_password_hash(formulario_criar_conta.senha.data)  # Gera um hash para a senha fornecida
        usuario = Usuario(email=formulario_criar_conta.email.data, nome=formulario_criar_conta.nome.data, senha=senha)  # Cria uma nova instância do usuário
        database.session.add(usuario)  # Adiciona o novo usuário à sessão do banco de dados
        database.session.commit()  # Salva as mudanças no banco de dados
        login_user(usuario, remember=True)  # Faz o login do novo usuário
        return redirect(url_for("perfil", id_usuario=usuario.id))  # Redireciona para a página de perfil do usuário
    return render_template("criar_conta.html", form=formulario_criar_conta)  # Renderiza o template de criação de conta com o formulário

# Define a rota para a página de perfil do usuário
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"]) # Permite que a página perfil tanto exiba o formulário de login (GET) quanto processe os dados enviados pelo formulário (POST)
@login_required  # Requer que o usuário esteja logado para acessar esta rota
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):  # Verifica se o ID do usuário na URL corresponde ao ID do usuário logado
        formulario_foto = FormFoto()  # Cria uma instância do formulário de upload de foto
        if formulario_foto.validate_on_submit():  # Verifica se o formulário foi enviado e é válido
            arquivo = formulario_foto.foto.data  # Obtém o arquivo de foto do formulário
            nome_seguro = secure_filename(arquivo.filename)  # Garante que o nome do arquivo é seguro
            caminho_arquivo = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_seguro)  # Define o caminho completo onde o arquivo será salvo
            arquivo.save(caminho_arquivo)  # Salva o arquivo no caminho definido
            foto = Foto(images=nome_seguro, id_usuario=current_user.id)  # Cria uma nova instância de Foto associada ao usuário atual
            database.session.add(foto)  # Adiciona a nova foto à sessão do banco de dados
            database.session.commit()  # Salva as mudanças no banco de dados
        return render_template("perfil.html", usuario=current_user, form=formulario_foto)  # Renderiza o template de perfil com o formulário de foto
    else:
        usuario = Usuario.query.get(int(id_usuario))  # Busca o usuário pelo ID fornecido na URL
        return render_template("perfil.html", usuario=usuario, form=None)  # Renderiza o template de perfil sem o formulário de foto

# Define a rota para logout
@app.route("/logout")
@login_required  # Requer que o usuário esteja logado para acessar esta rota
def logout():
    logout_user()  # Faz logout do usuário atual
    return redirect(url_for("homepage"))  # Redireciona para a página inicial

# Define a rota para o feed de fotos
@app.route("/feed")
@login_required  # Requer que o usuário esteja logado para acessar esta rota
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()  # Busca todas as fotos no banco de dados, ordenadas por data de criação em ordem decrescente
    return render_template("feed.html", fotos=fotos)  # Renderiza o template do feed com a lista de fotos
