# Importa as classes e validadores necessários do Flask-WTF e WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

# Importa o modelo Usuario do FakePinterest
from FakePinterest.models import Usuario

# Define o formulário de login
class FormLogin(FlaskForm):
    # Campo de entrada para o email com os validadores que garantem que o campo não esteja vazio e contenha um email válido
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    # Campo de entrada para a senha com o validador que garante que o campo não esteja vazio
    senha = PasswordField("Senha", validators=[DataRequired()])
    # Botão de submissão do formulário
    botao_confirmacao = SubmitField("Fazer Login")

    # Validador personalizado para o campo de email
    def validate_email(self, email):
        # Procura no banco de dados por um usuário com o email fornecido
        usuario = Usuario.query.filter_by(email=email.data).first()
        # Se nenhum usuário for encontrado, levanta um erro de validação
        if not usuario:
            raise ValidationError("Usuário não cadastrado. Faça cadastro para continuar.")

# Define o formulário de criação de conta
class FormCriarConta(FlaskForm):
    # Campo de entrada para o email com os validadores que garantem que o campo não esteja vazio e contenha um email válido
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    # Campo de entrada para o nome de usuário com o validador que garante que o campo não esteja vazio
    nome = StringField("Nome de Usuário", validators=[DataRequired()])
    # Campo de entrada para a senha com os validadores que garantem que o campo não esteja vazio e que a senha tenha entre 6 e 20 caracteres
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    # Campo de confirmação de senha com os validadores que garantem que o campo não esteja vazio e que corresponda ao campo de senha
    confirmacao_senha = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("senha")])
    # Botão de submissão do formulário
    botao_confirmacao = SubmitField("Criar Conta")

    # Validador personalizado para o campo de email
    def validate_email(self, email):
        # Procura no banco de dados por um usuário com o email fornecido
        usuario = Usuario.query.filter_by(email=email.data).first()
        # Se um usuário for encontrado, levanta um erro de validação
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar.")

# Define o formulário para upload de fotos
class FormFoto(FlaskForm):
    # Campo de entrada para o arquivo da foto com o validador que garante que o campo não esteja vazio
    foto = FileField("Foto", validators=[DataRequired()])
    # Botão de submissão do formulário
    botao_confirmacao = SubmitField("Enviar")
