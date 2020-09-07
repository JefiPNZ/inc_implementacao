from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tensorflow import keras
from gerencia_imagem import GerenciaImagem as gm

import tensorflow as tf
import numpy as np
import sys
import os 

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Tela(object):

    def __init__(self, parent=None):
        
        self.parent    = parent
        self.s_imagem  = ''

        #modelo
        self.model = tf.keras.models.load_model('modelo_teste_sem_flor')
        self.nome_classe = [
            'airplane', 'car', 'cat', 'dog', 'fruta', 'motorbike', 'person'
        ]

        #container
        self.container_superior = Frame(self.parent)
        self.container_inferior = Frame(self.parent)

        #componentes container superior
        self.btn_abre_img = Button(self.container_superior, text='abrir arquivo', command=self.abrir_arquivo)
        self.btn_analisa  = Button(self.container_superior, text='analisa', command=self.analisa)

        #componentes container inferior
        self.label_img = Label(self.container_inferior, text='imagem:')
        self.label_prv = Label(self.container_inferior, text='previsao:')

        #container superior
        self.btn_abre_img.pack()
        self.btn_analisa.pack()

        #container inferior
        self.label_img.pack()
        self.label_prv.pack()
        
        self.container_superior.pack()
        self.container_inferior.pack()

    def abrir_arquivo(self):
        self.s_imagem = filedialog.askopenfilename()
        self.label_img['text'] = f'imagem:{self.s_imagem}'

    def analisa(self):
        imagem = gm.abri_imagem(self.s_imagem)
        imagem = gm.redimenciona_imagem(imagem)
        imagem = np.array([imagem])

        predicao = self.model.predict(imagem)
        predicao_maior_confianca = np.argmax(predicao[0])
        self.label_prv['text'] = f'previsao:{self.nome_classe[predicao_maior_confianca]} {predicao_maior_confianca}'
        list_index = [0,1,2,3,4,5,6]
        for i in range(6):
            print()
            print(self.nome_classe[list_index[i]], ':', round(predicao[0][list_index[i]] * 100, 2), '%')

def main():
    root = Tk()
    Tela(root)
    # root.geometry('x50')
    root.resizable(width=0, height=0)
    root.mainloop()


if __name__ == '__main__':
    main()
    print('iniciado')
