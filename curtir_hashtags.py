# Importar as bibliotecas
import time  # Tempo de espera para "enganar" o Instagram
from random import randint  # Determinar o máximo de postagens curtidas da hashtag selecionada
from selenium import webdriver  # Criar o navegador
from selenium.webdriver.common.by import By  # Encontrar os elemento na página
from selenium.webdriver.chrome.service import Service  # Passar o driver para o selenium
from webdriver_manager.chrome import ChromeDriverManager  # Baixar automaticamente o driver do Chrome
from selenium.common.exceptions import NoSuchElementException  # Informar o erro que aparece


class CurtirHashtags:
    """
    Classe destinada a curtir postagens de uma determinada hashtag.
    """
    def __init__(self, usuario, senha, hashtag):
        # Usuário, senha e hashtag
        self.usuario = usuario
        self.senha = senha
        self.hashtag = hashtag

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

        # Pesquisar a hashtag
        self.pesquisar_hashtag()
        time.sleep(3)

        # Curtir as postagens
        self.curtir()
        time.sleep(1)

        # Fechar o navegador
        self.navegador.close()

        # Tempo de conclusão do trabalho do Bot
        tempo_final = (time.time() - tempo_inicio) / 60
        print(f'Tempo de execução do InstaBot: {tempo_final:.0f} minutos!')

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

    def pesquisar_hashtag(self):
        """
        Função destinada a acessar uma determinada hashtag do Instagram.
        """
        # Passar o link da hashtag desejada
        self.navegador.get(f'https://instagram.com/explore/tags/{self.hashtag}')

    def curtir(self):
        """
        Função destinada a curtir as postagens de uma determinada hasthtag.
        """
        # Clicar na primeira postagem da hashtag
        postagem = '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div[1]/div[2]'
        self.navegador.find_element(By.XPATH, postagem).click()
        time.sleep(2)

        # Loop para curtir de 80-100 fotos da hashtag específica
        maximo = randint(80, 101)
        contador = 0
        while True:
            # Curtir a foto
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
                print(f'Foram curtidas {contador} com a hashtag #{self.hashtag}')
                break
