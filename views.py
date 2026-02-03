from flask import render_template,request,redirect,session,flash,url_for,send_from_directory
from jogoteca import app,db
from models import Jogos,Usuarios
from helpers import recupera_imagem

@app.route('/')
def index():
    lista_jogos=Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)

@app.route('/cadastro-jogo/')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for(endpoint='login', proxima=url_for(endpoint='cadastro')))
    return render_template('cadastro.html',titulo='Cadastro de Jogo')

@app.route('/login')
def login():
    proxima=request.args.get('proxima',default='/',type=str)
    return render_template('login.html', proxima=proxima)

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

    arquivo=request.files['arquivo']
    upload_path=app.config['UPLOAD_PATH']
    arquivo.save(f"{upload_path}/capa_{novo_jogo.id}.jpg")

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima='editar'))
    jogo=Jogos.query.filter_by(id=id).first()
    capa_jogo=recupera_imagem(id)
    return render_template('editar.html',titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/atualizar',methods=['POST'])
def atualizar():
    jogo=Jogos.query.filter_by(id=request.form['id_jogo']).first()
    jogo.nome=request.form['nome']
    jogo.categoria=request.form['categoria']
    jogo.console=request.form['console']

    db.session.add(jogo)
    db.session.commit()

    arquivo=request.files['arquivo']
    upload_path=app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa_{jogo.id}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Jogos.query.filter_by(id=id).delete()

    db.session.commit()

    flash('Jogo deletado com sucesso!')
    return redirect(url_for('index'))

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

@app.route('/uploads/<nome_arquivo>')
def capa_padrao(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)



