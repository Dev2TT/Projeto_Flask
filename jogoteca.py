from flask import Flask, render_template,request,redirect,session,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.secret_key='@vic%'

app.config.from_object(Config)
db=SQLAlchemy(app)

class Jogos(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome=db.Column(db.String(200), nullable=False)
    categoria=db.Column(db.String(20),nullable=False)
    console=db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Name {self.nome}>"
    

class Usuarios(db.Model):
    nome=db.Column(db.String(200),nullable=False)
    nickname=db.Column(db.String(200),primary_key=True)
    senha=db.Column(db.String(40),nullable=False)
    id_jogos=db.Column(db.Integer,db.ForeignKey(Jogos.id))

    def __repr__(self):
        return f"<Name {self.nome}>"



@app.route('/')
def index():
    lista_jogos=Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)

@app.route('/cadastro-jogo/')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for(endpoint='login', proxima=url_for(endpoint='cadastro')))
    return render_template('cadastro.html',titulo='Cadastro de Jogo')

@app.route('/criar-jogo',methods=['POST'])
def criar_jogo():
    nome=request.form['nome']
    categoria=request.form['categoria']
    console=request.form['console']
    
    jogo=Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash(f"O jogo já existe!")
        return redirect(url_for('index'))

    novo_jogo=Jogos(nome=nome,categoria=categoria,console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima=request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar',methods=['POST'])
def autenticar():
    usuario=Usuarios.query.filter_by(nickname= request.form['usuario']).first()
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado']=request.form['usuario']
            flash(f'{session['usuario_logado']} Logado com Sucesso!')
            proxima_pagina=request.form['proximo']
            return redirect(proxima_pagina)
    flash('Dados incorretos! Verifique e tente novamente.')
    return redirect(url_for(endpoint='login'))
    
@app.route('/logout')
def logout():
    if session['usuario_logado'] == None:
        flash(f'Não há usuário logado no momento.')
        return redirect(url_for(endpoint='login'))
    flash(f'{session['usuario_logado']} Deslogado.')
    session['usuario_logado']=None
    return redirect(url_for(endpoint='login'))

app.run(debug=True)