from flask import Flask, render_template,request,redirect,session,flash,url_for
from jogo import Jogo
from usuario import Usuario

app = Flask(__name__)
app.secret_key='@vic%'

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista_jogos = [jogo1,jogo2,jogo3]

usuario1=Usuario('Katia','Kat','20321')
usuario2=Usuario('Certezas','correto','incorreto')
usuario3=Usuario('Patricia', 'Mal', 'Bem')

lista_usuarios=[usuario1,usuario2,usuario3]

@app.route('/')
def index():
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
    novo_jogo=Jogo(nome,categoria,console)
    lista_jogos.append(novo_jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proximo=request.args.get('proxima')
    return render_template('login.html', proxima=proximo)

@app.route('/autenticar',methods=['POST'])
def autenticar():
    for usuario in lista_usuarios:
        if usuario.nickname == request.form['usuario'] and usuario.senha == request.form['senha']:
            session['usuario_logado']=request.form['usuario']
            flash(f'{session['usuario_logado']} Logado com Sucesso!')
            proxima_pagina=request.form['proxima']
            return redirect(proxima_pagina)
    flash('Dados incorretos! Verifique e tente novamente.')
    return redirect(url_for(endpoint='login'))
    
@app.route('/logout')
def logout():
    flash(f'{session['usuario_logado']} Deslogado.')
    session['usuario_logado']=None
    return redirect(url_for(endpoint='login'))

app.run(debug=True)