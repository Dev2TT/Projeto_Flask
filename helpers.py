import os
from jogoteca import app

def recupera_imagem(nome):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if(f'capa_{nome}.jpg' == nome_arquivo):
            return nome_arquivo
    
    return 'capa_padrao.jpg'