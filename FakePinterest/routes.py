from flask import render_template, url_for, redirect, flash
from FakePinterest import app, database, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from FakePinterest.forms import FormCriarConta, FormLogin, FormFoto
from FakePinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def homepage():
    formulario_login = FormLogin()
    if formulario_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formulario_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formulario_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))  # Certifique-se de passar id_usuario aqui
    return render_template("homepage.html", form=formulario_login)

@app.route("/criar_conta", methods=["GET", "POST"])
def criarconta():
    formulario_criar_conta = FormCriarConta()
    if formulario_criar_conta.validate_on_submit():
        print("Dados do formulário:", formulario_criar_conta.email.data, formulario_criar_conta.nome.data, formulario_criar_conta.senha.data)
        senha = bcrypt.generate_password_hash(formulario_criar_conta.senha.data)
        usuario = Usuario(email=formulario_criar_conta.email.data, nome=formulario_criar_conta.nome.data, senha=senha)
        
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))  # Certifique-se de passar id_usuario aqui
    return render_template("criar_conta.html", form=formulario_criar_conta)


@app.route("/perfil/<id_usuario>", methods = ["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        formulario_foto = FormFoto()
        if formulario_foto.validate_on_submit():
            
            arquivo = formulario_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho_arquivo = os.path.join (os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho_arquivo)
            foto = Foto(images = nome_seguro, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form = formulario_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form = None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos = fotos)