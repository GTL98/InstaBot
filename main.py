# Importar os módulos do InstaBot
from deixar_seguir import DeixarSeguir
from curtir_hashtags import CurtirHashtags

# Informar qual ação o InstaBot fará
acao = 0

# Informar login, senha e hashtag
login = ''
senha = ''
hashtag = ''

if __name__ == '__main__':
    if acao == 0:
        DeixarSeguir(login, senha)
    elif acao == 1:
        CurtirHashtags(login, senha, hashtag)
