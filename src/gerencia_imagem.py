import cv2 as cv
import numpy as np

class GerenciaImagem(object):

    @staticmethod
    def abri_imagem(caminho, cinza=False):
        '''
            Nome do arquivo a ser aberto
              Args:
                 caminho: caminho da imagem a ser aberta. 
                 retorna (object)imagem
        '''
        if cinza:
            return cv.imread(caminho, cv.IMREAD_GRAYSCALE)
        return cv.imread(caminho)

    @staticmethod
    def redimenciona_imagem(imagem, dimensao=(40, 40)):
        '''
            Cria uma nova imagem com a dimensao informada
            com a imagem anterior.
                Args:
                   imagem: objeto imagem a ser redimensionado.
                   dimensao: tupla com as novas dimensões
                   retorna (objeto) imagem
        '''
        return cv.resize(imagem, dimensao)

    @staticmethod
    def muda_cor_imagem_cinza(imagem):
        '''
            Muda a cor da imagem para cinza
                Args:
                    imagem: objeto imagem a ter sua cor alterada.
                    retorna (object) imagem
        '''
        #é necessário converter o array da imagem em float32, porque
        #o metodo utilizado para mudar o esquema de cores so aceita float32
        img = np.float32(imagem)
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    @staticmethod
    def salva_imagem(imagem, nome='img.jpg'):
        '''
            Imagem a ser salva
               Args:
                  nome: nome com o qual salvar a imagem.
                  extensao: extensão do arquivo a ser salvo
                  imagem: imagem a ser salva
        '''
        cv.imwrite(f'{nome}',imagem)

    @staticmethod
    def mostra_imagem(nome, imagem):
        '''
            Mostra a imagem em um frame.
                Args:
                    nome: string nome do frame
                    imagem: objeto imagem a ser mostrado na tela
        '''
        cv.imshow(nome, imagem)