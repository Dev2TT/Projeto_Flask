from jogoteca import db

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

