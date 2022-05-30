# Importar os módulos do InstaBot
from deixar_seguir import DeixarSeguir
from curtir_hashtags import CurtirHashtags
from curtir_postagens_perfil import CurtirPerfil

# Informar qual ação o InstaBot fará
acao = 1

# Informar login, senha e hashtag
login = ''
senha = ''
perfil = ''
hashtag = ''
quantidade_curtir = 0

if __name__ == '__main__':
    if acao == 1:
        DeixarSeguir(login, senha)
    elif acao == 2:
        CurtirHashtags(login, senha, hashtag, quantidade_curtir)
    elif acao == 3:
        CurtirPerfil(login, senha, perfil, quantidade_curtir)
