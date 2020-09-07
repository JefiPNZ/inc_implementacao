import time
import requests#serve para fazer requisições
import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from unicodedata import normalize

from gerencia_arquivo import GerenciaArquivo

class ManipuladorBrowser(object):

    TEMPO_ESPERA = 3 #quantidade em segundos q o algoritmo deve esperar antes de continuar sua execução
    NOME_PASTA   = 'dataset'

    _options     = None
    _driver      = None
    _termo_busca = ''

    def __init__(self):
        self._options          = Options()
        self._options.headless = False
        self._driver           = webdriver.Chrome(options=self._options)
        self._termo_busca      = 'teste'

    def scroll_down(self):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self._espera()

    def fecha(self):
        self._driver.close()
        self._driver.quit()

    def _espera(self):
        '''
            Para a execução do algoritmo por um determinado tempo
        '''
        time.sleep(self.TEMPO_ESPERA)

    def navega_para(self, url):
        '''
            Vai para a pagina da url informada
                Args:
                    url: url para qual ser direcionado
        '''
        self._driver.get(url)

    def cria_nova_guia(self):
        '''
            Cria uma nova guia e muda para ela
        '''
        
        self._driver.execute_script("window.open()")
        janelas = self._driver.window_handles
        self._driver.switch_to.window(janelas[len(janelas)-1])

    def get_codigo_fonte_pagina_atual(self):
        return self._driver.page_source
    
    def pesquisa_google(self, termo_pesquisa):
        '''
            Pesquisa um termo no google
                Args:
                   termo_pesquisa: termo a ser pesquisado no google
                   return (string) codigo fonte da pagina
        '''
        self._termo_busca = termo_pesquisa
        self.navega_para('http://google.com/')
        print('> [image_download] aguardando carregamento da pagina...')
        self._espera()

        #essa é barra de pesquisa do google
        barra_pesquisa = self._driver.find_element_by_name('q')
        #digita o termo na barra de busca
        barra_pesquisa.send_keys(termo_pesquisa)
        barra_pesquisa.submit()
        print('> [image_download] aguardando carregamento da pagina...')
        self._espera()

    def seleciona_imagens(self):
        '''
            Seleciona a opção imagens q aparece logo abaixo da
            barra de pesquisas
        '''
        elemento  = self._driver.find_element_by_id('hdtb-msb-vis')
        elementos = elemento.find_elements_by_tag_name('a')
        for elem in elementos:
            if elem.text.lower() == 'imagens':
                elem.click()
                break
    
    def get_link_imagens(self):
        '''
            Retorna o link de todas as imagens na tela
                Args:
                   retorna (array) de links
        '''
        links = []

        # for i in range(5):
        #elemento no qual estao contidas todas as imagens q aparecem
        elemento  = elemento  = self._driver.find_element_by_id('islmp')
        #pega todas as tag 'a'
        elementos = elemento.find_elements_by_tag_name('a')

        for elem in elementos:
            try:
                img  = elem.find_element_by_tag_name('img')
                link = img.get_attribute('src')
                if link in links:
                    continue
                print('buscando link da imagem...')
                links.append(link)
            except:
                continue
            # self.scroll_down()
        
        return links

    
    def baixa_imagem_url(self, imagens):
        '''
            Baixa a imagem da url passada
                Args:
                   imagens: array com as urls das imagens a serem baixadas
        '''
        s_dir = normalize('NFKD', self._termo_busca).encode('ASCII','ignore').decode('ASCII')

        if not GerenciaArquivo.existe_diretorio(self.NOME_PASTA):
            GerenciaArquivo.cria_diretorio(self.NOME_PASTA)

        if not GerenciaArquivo.existe_diretorio(f'{self.NOME_PASTA}/{s_dir}'):
            GerenciaArquivo.cria_diretorio(f'{self.NOME_PASTA}/{s_dir}')

        cont  = 0
        for imagem in imagens:
            if not type(imagem) is str:
                continue

            resp = urllib.request.urlopen(imagem)
            with open(f'{self.NOME_PASTA}/{s_dir}/{s_dir}_{cont}.jpg', 'wb') as arquivo:
                try:
                    arquivo.write(resp.file.read())
                    print('baixando imagem...')
                except:
                    continue
            cont += 1
        print(f'quantidade de imagens:{cont}')