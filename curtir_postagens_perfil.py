# Importar as bibliotecas
import time  # Tempo de espera para "enganar" o Instagram
from random import randint  # Determinar o máximo de postagens curtidas da hashtag selecionada
from selenium import webdriver  # Criar o navegador
from selenium.webdriver.common.by import By  # Encontrar os elemento na página
from selenium.webdriver.chrome.service import Service  # Passar o driver para o selenium
from webdriver_manager.chrome import ChromeDriverManager  # Baixar automaticamente o driver do Chrome
from selenium.common.exceptions import NoSuchElementException  # Informar o erro que aparece


class CurtirPerfil:
    """
    Classe destinada a curtir fotos de perfis do Instagram.
    """
    def __init__(self, usuario, senha, perfil, quantidade_curtir):
        # Usuário, senha, conta e quantidade de curtidas
        self.usuario = usuario
        self.senha = senha
        self.perfil = perfil
        self.quantidade_curtir = quantidade_curtir

        # Tempo quando o InstaBot foi ligado
        tempo_inicio = time.time()

        # Indicar o driver do Chrome
        servico = Service(ChromeDriverManager().install())
        # Criar o navegador
        self.navegador = webdriver.Chrome(service=servico)
        # Acessar o Instagram
        self.navegador.get('https://instagram.com')
        time.sleep(1)

        # Entrar com login, senha e acessar a página inicial do Instagram
        self.pagina_inicial_instagram()
        time.sleep(2)

        # Pesquisar o peril
        self.pesquisar_perfil()
        time.sleep(3)

        # Curtir as postagens
        self.curtir()
        time.sleep(1)

        # Fechar o navegador
        self.navegador.close()

    def pagina_inicial_instagram(self):
        """
        Função destinada a entrar com login e senha do usuário para acessar a página inicial do Instagram
        """
        # XPath do login
        campo_login = '//*[@id="loginForm"]/div/div[1]/div/label/input'
        self.navegador.find_element(By.XPATH, campo_login).send_keys(self.usuario)
        time.sleep(2)

        # XPath da senha
        campo_senha = '//*[@id="loginForm"]/div/div[2]/div/label/input'
        self.navegador.find_element(By.XPATH, campo_senha).send_keys(self.senha)
        time.sleep(2)

        # XPath do botão para logar
        botao_login = '//*[@id="loginForm"]/div/div[3]/button'
        self.navegador.find_element(By.XPATH, botao_login).click()
        time.sleep(5)

        # XPath do botão "Agora não" para salvar as informações no navegador
        botao_agora_nao_1 = '//button[contains(text(), "Agora não")]'
        self.navegador.find_element(By.XPATH, botao_agora_nao_1).click()
        time.sleep(2)

        # XPath do botão "Agora não" para o navegador mandar notificações
        botao_agora_nao_2 = '//button[contains(text(), "Agora não")]'
        self.navegador.find_element(By.XPATH, botao_agora_nao_2).click()

    def pesquisar_perfil(self):
        """
        Função destinada a acessar um determinado perfil do Instagram
        """
        # Passar o link do perfil desejado
        self.navegador.get(f'https://instagram.com/{self.perfil}')

    def curtir(self):
        """
        Função destinada a curtir as fotos de um determinado perfil
        """
        # Saber quantas postagens o perfil tem
        publicacoes = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/div/span'
        p = self.navegador.find_element(By.XPATH, publicacoes).text
        p_novo = p.replace('.', '')
        p_int = int(p_novo)

        # Saber se o perfil possui o mínimo de publicações selecionado para curtir as fotos
        maximo = 0
        if self.quantidade_curtir > p_int:
            maximo = p_int
        elif self.quantidade_curtir < p_int:
            maximo = self.quantidade_curtir

        # Clicar na primeira postagem do perfil
        postagem = '//*[@id="react-root"]/section/main/div/div[3]/article/' \
                   'div[1]/div/div[1]/div[1]/a/div[1]/div[2]'
        self.navegador.find_element(By.XPATH, postagem).click()
        time.sleep(2)

        # Loop para curtir o número de fotos desejada ou o máximo de postagens no perfil
        contador = 0
        while True:
            # Curtir a publicação
            curtir_foto = '/html/body/div[6]/div[3]/div/article/div/div[2]/' \
                          'div/div/div[2]/section[1]/span[1]/button'
            self.navegador.find_element(By.XPATH, curtir_foto).click()
            time.sleep(1)
            contador += 1

            # Avançar para a próxima postagem
            try:
                proxima_postagem = '/html/body/div[6]/div[2]/div/div[2]/button'
                self.navegador.find_element(By.XPATH, proxima_postagem).click()
            except NoSuchElementException:
                proxima_postagem = '/html/body/div[6]/div[2]/div/div/button'
                self.navegador.find_element(By.XPATH, proxima_postagem).click()
            time.sleep(2)
            if contador == maximo:
                print(f'Foram curtidas {contador} publicações no perfil {self.perfil}')
                break
