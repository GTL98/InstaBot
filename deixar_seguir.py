# Importar as bibliotecas
import time  # Tempo de espera para "enganar" o Instagram
from random import randint  # Determinar o máximo de contas que serão deixadas de seguir
from selenium import webdriver  # Criar o navegador
from selenium.webdriver.common.by import By  # Encontrar os elementos na página
from selenium.webdriver.chrome.service import Service  # Passar o driver para o selenium
from webdriver_manager.chrome import ChromeDriverManager  # Baixar automaticamente o driver do Chrome
from selenium.common.exceptions import NoSuchElementException  # Informar o erro que aparece


class DeixarSeguir:
    """
    Classe destinada a ser um robô para o Instagram. Suas funções são:
        - Seguir contas;
        - Dar like em fotos de hashtags;
        - Dar like em fotos de contas específicas e
        - Deixar de seguir contas que não seguem de volta;
    """
    def __init__(self, usuario, senha):
        # Usuário e senha
        self.senha = senha
        self.usuario = usuario

        # Tempo quando o Bot foi ligado
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
        time.sleep(1)

        # Entrar no seu perfil do Instagram
        self.acessar_seu_perfil()
        time.sleep(5)

        # Acessar "seguidores" e criar uma lista com todos os seguidores da conta
        seguidores = self.acessar_seguidores()
        time.sleep(2)

        # Acessar "seguindo" e criar uma lista com todas as contas que seguimos
        seguindo = self.acessar_seguindo()
        time.sleep(2)

        # Deixar de seguir as conta que não seguem de volta de modo automático
        self.deixar_seguir(seguidores, seguindo)

        # Tempo de conclusão do trabalho do Bot
        tempo_final = (time.time() - tempo_inicio) / 60
        print(f'Tempo de execução do InstaBot: {tempo_final:.0f} minutos!')

    def pagina_inicial_instagram(self):
        """
        Função destinada à entrar com o login e senha do usuário e acessar a página inicial do Instagram.
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
        botao_agora_nao_1 = '//*[@id="react-root"]/section/main/div/div/div/div/button'
        self.navegador.find_element(By.XPATH, botao_agora_nao_1).click()
        time.sleep(2)

        # Nome da classe do botão "Agora não" para o navegador mandar notificações
        botao_agora_nao_2 = 'aOOlW.HoLwm'
        self.navegador.find_element(By.CLASS_NAME, botao_agora_nao_2).click()
        time.sleep(2)

    def acessar_seu_perfil(self):
        """
        Função destinada à entrar no seu perfil do Instagram.
        """
        # Encontrar o acesso ao perfil na página inicial
        perfil = f'//a[contains(@href, "{self.usuario}")]'
        self.navegador.find_element(By.XPATH, perfil).click()

    def acessar_seguidores(self):
        """
        Função destinada à criar uma lista com todas as contas em 'seguidores'.
        :return lista com todas as contas de 'seguidores':
        """
        # Acessar a página das contas
        seguidores = f'//a[contains(@href, "{self.usuario}/followers")]'
        self.navegador.find_element(By.XPATH, seguidores).click()
        time.sleep(2)

        # Botão "Remover"
        botao = '//li[1]/div/div[3]/button'
        time.sleep(2)

        # Criar a lista com todos os seguidores
        contas_seguidores = self.obter_contas(botao, 'seguidores')

        # Retornar uma lista com todos os seguidores
        return contas_seguidores

    def acessar_seguindo(self):
        """
        Função destinada à criar uma lista com todas as contas em 'seguindo'.
        :return lista com todas as contas em 'seguindo':
        """
        # Acessar a página das contas
        seguindo = f'//a[contains(@href, "{self.usuario}/following")]'
        self.navegador.find_element(By.XPATH, seguindo).click()
        time.sleep(2)

        # Botão "Seguindo"
        botao = '//li[1]/div/div[3]/button'

        # Criar uma lista com todas as contas que seguimos
        contas_seguindo = self.obter_contas(botao, 'seguindo')

        # Retornar uma lista com as contas que seguimos
        return contas_seguindo

    def obter_contas(self, botao, pagina):
        """
        Função destinada a obter o nome de todas as contas em "seguidores" e "seguindo" sempre que chamada.
        :param botao:
        :param pagina:
        :return lista com todos os nomes das contas de "seguidores" e "seguindo" sempre que chamada:
        """

        # Descer a página das contas sempre que um novo botão aparecer
        self.navegador.execute_script('arguments[0].scrollIntoView', botao)
        time.sleep(2)

        # XPath da barra de navegação
        if pagina == 'seguidores':
            xpath_barra_navegacao = '/html/body/div[6]/div/div/div/div[2]'
        elif pagina == 'seguindo':
            xpath_barra_navegacao = '/html/body/div[6]/div/div/div/div[3]'
        barra_navegacao = self.navegador.find_element(By.XPATH, xpath_barra_navegacao)

        # Continuar descendo a página das contas até chegar ao fim
        ultima_altura, altura = 0, 1  # Altura da página das contas
        while ultima_altura != altura:
            ultima_altura = altura
            time.sleep(2)
            altura = self.navegador.execute_script(
                '''arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight''', barra_navegacao
            )

        # Colocar em uma lista o nome das contas
        tag = 'a'
        contas = barra_navegacao.find_elements(By.TAG_NAME, tag)
        nomes = [nome.text for nome in contas if nome.text != '']
        time.sleep(2)

        # Fechar a janela das contas
        botao_fechar = '/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button'
        self.navegador.find_element(By.XPATH, botao_fechar).click()

        # Retornar o a lista com os nomes
        return nomes

    def deixar_seguir(self, seguidores, seguindo):
        """
        Função destinada a deixar de seguir as contas que não seguem de volta.
        :param seguidores:
        :param seguindo:
        :return automatização para deixar de seguir as contas que não seguem de volta:
        """
        # Criar uma lista com todas as contas que não seguem de volta
        nao_segue_volta = [usuario for usuario in seguindo if usuario not in seguidores]

        # Determinar um máximo de contas que serão deixadas de seguir
        maximo = randint(30, 41)
        contador = 0

        # Deixar de seguir as contas que não segue de volta
        for conta in nao_segue_volta:
            # Usar o link que fica mais fácil de acessar as contas que não seguem de volta
            self.navegador.get(f'https://instagram.com/{conta}/')
            time.sleep(5)
            while True:
                try:
                    botao = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]' \
                            '/div/div[2]/div/span/span[1]/button'
                    self.navegador.find_element(By.XPATH, botao).click()
                    time.sleep(2)
                except NoSuchElementException:
                    print(f'Conta para deixar de seguir manualmente: {conta}')
                    time.sleep(2)
                    break
                else:
                    botao_deixar_seguir = '//button[contains(text(), "Deixar de seguir")]'
                    self.navegador.find_element(By.XPATH, botao_deixar_seguir).click()
                    contador += 1
                    time.sleep(5)
                    self.navegador.refresh()
                    time.sleep(5)
                    break

            if contador == maximo:
                print(f'Deixamos de seguir {contador} contas!')
                time.sleep(2)
                self.navegador.close()
                break
