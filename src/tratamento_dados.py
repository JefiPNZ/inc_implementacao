from gerencia_imagem import GerenciaImagem as imagem
from gerencia_arquivo import GerenciaArquivo as arquivo
from manipulador_browser import ManipuladorBrowser
from unicodedata import normalize
import random
import json

class TratamentoDados(object):

    ARQUIVO_JSON = 'data.txt'

    _debug         = None
    _dataset       = None#diretorio do dataset de onde pegar as imagens
    _dataset_norm  = None#diretorio do dataset normalizado
    _labels        = None#labels a seram colocados nas imagens indicando o que elas são
    _termos        = None#Termos para se fazer a busca da imagens no google
    _json          = None#json onde os dados das imagens tratadas sao armazenados
    _grupos        = None#array de grupo onde ficam cada imagem
    _class_names   = None#classes utilizadas
    _modelo_treino = None#modelo de treino gerado no fim do processamento
    _modelo_teste  = None#modelo de teste gerado no fim do processamento
   
    _manipulador_browser = None#objeto q permite a manipulacao do browser por codigo

    def __init__(self):
        self._dataset       = ''
        self._dataset_norm  = 'dataset_norm'
        self._labels        = {}
        self._json          = []
        self._debug         = False
        self._grupos        = {}
        self._modelo_treino = []
        self._modelo_teste  = []
        self._class_names   = []

    def limpa_dataset_norm(self):
        try:
            arquivo.remove(self._dataset_norm)
        except:
            pass

    def set_termos(self, arr):
        '''
        Define os termos de pesquisa no google
        para baixar imagens
        '''
        self._termos = arr

    def _get_manipulador_browser(self):
        if self._manipulador_browser is None:
            self._manipulador_browser = ManipuladorBrowser()
        return self._manipulador_browser

    def set_debug(self, bDebug):
        self._debug = bDebug
    
    def set_dataset_path(self, path):
        '''
        Define o diretorio de onde buscar as imagens
        '''
        self._dataset = arquivo.get_path(path)
    
    def get_dataset_path(self):
        '''
        Retorna o diretorio de onde pegar as imagens,
        caso o diretorio nao tenha sido defino dispara uma 
        exceção
        '''
        if self._dataset is None:
            raise Exception('Não foi definido um deiretório de dataset de onde buscar as imagens')
        return self._dataset
    
    def get_dataset_norm_path(self):
        '''
        Retorna o diretorio de onde pegar as imagens,
        caso o diretorio nao tenha sido defino dispara uma 
        exceção
        '''
        if self._dataset_norm is None:
            raise Exception('Não foi definido um deiretório de dataset normalizado de onde buscar as imagens')
        return self._dataset_norm

    def get_labels(self):
        '''
        Retorna um array assossiativo de labels
        '''
        if self._labels is None:
            raise Exception('Não foi definido nenhum label')
        return self._labels

    def get_grupos(self):
        '''
        Retorna um dict dos grupos onde cada posição é um array
        '''
        if self._grupos is None:
            raise Exception('Os grupos não foram carregados')
        return self._grupos

    def get_class_names(self):
        '''
        Retorna um dict dos grupos onde cada posição é um array
        '''
        if self._class_names is None:
            raise Exception('Os grupos não foram carregados')
        return self._class_names

    def get_json(self):
        '''
        Retorna o json com os dados das imagens tratadas
        '''
        if len(self._json) > 0:
            return self._json
        data_json = json.loads(arquivo.abrir_arquivo_texto(self.ARQUIVO_JSON))
        return data_json

    def processa_labels(self, bCarrega=True):
        '''
        Trata os labels que serão utilizados no 
        treinamento
            Args:
                bCarrega: boolean q indica de carrega os labels a partir dos nommes
                contidos nas pastas dentro do dataset
        '''
        self._trata_labels(bCarrega)
        self._trata_grupos()
        self._trata_class_names()
        print('labels processados')


    def processa_imagens(self):
        '''
        Faz o tratamento inicial antes de mandar as imagens 
        para a rede neural
        '''
        self._cria_dir_imagens_normalizadas()
        self._trata_imagens()
        #salva o json das imagens no diretorio raiz
        arquivo.salva_arquivo_texto('data', 'txt', json.dumps(self._json))
        print('imagens processadas')
    
    def processa_dados(self):
        '''
        Faz o processamento dos dados, divide os dados em 
        dois modelos um de teste e outro de treino
        '''
        self._trata_dados()
        self._carrega_modelos()
        print('dados processados')

    def _trata_labels(self, bCarrega):
        '''
        Trata os labels a serem utilizados 
        para descrever  as imagens
        '''
        if bCarrega:
            iCont = 0
            for arq in self.get_dataset_path().iterdir():
                self._labels[f'{arq.name}'] = iCont
                iCont += 1
        else:    
            for numero, label in enumerate(self._termos):
                #tira acentos
                label = normalize('NFKD', classe).encode('ASCII','ignore').decode('ASCII')
                self._labels[f'{label}'] = numero
                    
        if self._debug:
            print('Labels:')
            print(self._labels)

    def _trata_grupos(self):
        '''
        Cria o grupo de cada label
        '''
        labels = self.get_labels()
        for numero, label in enumerate(labels):
            self._grupos[f'{numero}'] = []
        if self._debug:
            print('Grupos:')
            print(self._grupos)

    def _trata_class_names(self):
        '''
        Cria o grupo de cada label
        '''
        labels = self.get_labels()
        for chave in labels.keys():
            self._class_names.append(chave)
        if self._debug:
            print('Class Names:')
            print(self._class_names)


    def _cria_dir_imagens_normalizadas(self):
        '''
        Cria um diretorio para as imagens tratadas
        '''
        self._dataset_norm = arquivo.get_path(self._dataset_norm)

    def _trata_imagens(self):
        '''
        Faz todo o pre-processamento inicial nas imagens
        '''
        for arq in self.get_dataset_path().iterdir():
            if not arquivo.existe_diretorio(f'{self.get_dataset_norm_path().absolute()}/{arq.name}'):
                arquivo.cria_diretorio(f'{self.get_dataset_norm_path().absolute()}/{arq.name}')

            self._normaliza_imagem(arq)
        
    def _normaliza_imagem(self, oDir):
        '''
        Faz todo o tratamento das imagens para deixa-las
        no formato q a rede neural espera
        '''
        nome_dir = oDir.name#tipo da imagem
        cont     = 0
        for arq in oDir.iterdir():
            imagem_original = imagem.abri_imagem(f'{arq.absolute()}')
            if imagem_original is None:
                continue
            imagem_resize = imagem.redimenciona_imagem(imagem_original)
            #salva a imagem no diretorio passado
            imagem.salva_imagem(imagem_resize, f'{self.get_dataset_norm_path().absolute()}/{nome_dir}/{arq.name}')
            self._json.append({
                'tipo'   : nome_dir,
                'caminho': f'{self._dataset_norm.absolute()}/{nome_dir}/{arq.name}',
                'label'  : self.get_labels()[nome_dir]
            })
            if self._debug:
                print(f'processando imagem {nome_dir}/{cont}')
                cont += 1
                

    def _trata_dados(self):
        self._divide_grupo(self._converte_dados_tupla(self.get_json()))

        oGrupos = self.get_grupos()
        for grupo in oGrupos.items():
            oGrupos[grupo[0]] = self._trata_grupo(grupo[1], 30)

    def _converte_dados_tupla(self, dados):
        '''
            Coloca os dados passados em uma tupla
                Args:
                    data: dict com dados
                    return (array) tuplas
        '''
        aDadosTratados = []
        for dado in dados:
            aDadosTratados.append((
                dado['tipo'],
                imagem.abri_imagem(dado['caminho']),
                dado['label']
            ))
        if self._debug:
            print('dados tratados')
            print(aDadosTratados)
        return aDadosTratados
    
    def _divide_grupo(self, dados):
        '''
            coloca cada dado em um array correspondente 
            a seu label
        '''
        oGrupos = self.get_grupos()
        for dado in dados:
            grupo = oGrupos[f'{dado[2]}']
            grupo.append(dado)
    
    def _trata_grupo(self, arr, porc_teste):
        '''
        Divide um array em dois modelos o de treino e o de teste
        Args:
            arr: array a ser divido
            porc: porcentagem das noticias a serem usadas para testes
            return tupla
        '''
        random.shuffle(arr)

        qtd_dados =  int(len(arr) - (len(arr)*(porc_teste/100)))

        a_treino = arr[:qtd_dados]
        a_teste  = arr[qtd_dados:]

        if self._debug:
            total = len(arr)
            print('\n')
            print('='*20)
            print(f'Dados do array de {arr[0][0]}')
            print('='*20)
            print(f'quantidade total de dados: {total}')
            print(f'porcentagem de dados usados para teste: {porc_teste}%')
            print(f'quantidade de dados usados para treino: {total - (total*(porc_teste/100))}')
            print(f'quantidade de dados usados para teste: {(total*(porc_teste/100))}')
            print('='*20)
            print(f'Modelo de treino')
            print(f'quantidade de dados esperada no modelo de treino: {total - (total*(porc_teste/100))}')
            print(f'quantidade de dados no modelo de treino: {len(a_treino)}')
            print('='*20)
            print(f'Modelo de teste')
            print(f'quantidade de dados esperada no modelo de teste: {(total*(porc_teste/100))}')
            print(f'quantidade de dados no modelo de teste: {len(a_teste)}')


        return (a_treino, a_teste)
    
    def _carrega_modelos(self):
        '''
            carrega os modelos de treino e teste
        '''
        oGrupos = self.get_grupos()
        for grupo in oGrupos.items():
            self._juncao_array(self._modelo_treino, grupo[1][0])
            self._juncao_array(self._modelo_teste , grupo[1][1])
    
    def _juncao_array(self, a_destino, a_fonte):
        '''
            Coloca todos os dados do array fonte no array de destino
                Args:
                    a_destino: array de destino
                    a_fonte: array de origem
        '''
        for elem in a_fonte:
            a_destino.append(elem)

    def get_modelos(self):
        a_treino       = []
        a_treino_label = []

        a_teste       = []
        a_teste_label = []

        for dado in self._modelo_treino:
            a_treino.append(dado[1])
            a_treino_label.append(dado[2])

        for dado in self._modelo_teste:
            a_teste.append(dado[1])
            a_teste_label.append(dado[2])

        return ((a_treino, a_treino_label), (a_teste, a_teste_label))
    
    def _pesquisa_termos(self):
        '''
        pesquisa os termos passados no google
        '''
        for termo in self._termos:
            self._pesquisa_termo_baixa_imagem(termo)
        self._get_manipulador_browser().fecha()
    
    def _pesquisa_termo_baixa_imagem(self, termo):
        '''
        Baixa as imagens encontradas q correspondem ao termo da 
        pesquisa
        '''
        mb = self._get_manipulador_browser()
        mb.pesquisa_google(termo)
        mb.seleciona_imagens()

        links = mb.get_link_imagens()
        #baixa as imagens e salva em um diretorio especifico
        mb.baixa_imagem_url(links)