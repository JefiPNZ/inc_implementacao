import sys
import tensorflow        as tf
import numpy             as np
import matplotlib.pyplot as plt

from tensorflow       import keras
from keras.models     import Sequential
from keras.layers     import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from keras.utils      import to_categorical

from tratamento_dados import TratamentoDados
from gerencia_imagem  import GerenciaImagem as gm

def modelo1():
    #arquitetura do modelo
    #O modelo sequential agrupa um conjunto de camadas de forma linear
    model = Sequential()

    #adiciona a primeira camada da rede
    #Camada de convolução 2D (convolução espacial sobre imagens).
    model.add(
        Conv2D(
            filters=32,
            kernel_size=(3,3),
            activation='relu', 
            input_shape=shape_input#tipo do formato de dados esperado
        )
    )
    #adiciona um pooling layer O pooling é necessário para 
    # reduzir a amostra da detecção de recursos em mapas de recursos.
    model.add(MaxPooling2D(pool_size=(2,2)))

    #adiciona um flatenning layer
    model.add(Flatten())

    #adicionando uma camada com n neuronios
    model.add(Dense(1600, activation='relu'))

    #adiciona primeira camada de saida, diminui os neronios pela metade
    model.add(Dropout(0.5))

    #adicionando uma camada com n neuronios
    model.add(Dense(800, activation='relu'))

    #adicionando uma camada com 10 neuronios, para as 10 classes diferentes de arquivos
    model.add(Dense(qtd_class, activation='softmax'))

    #compilando o modelo
    model.compile(
        loss = 'categorical_crossentropy',
        optimizer = 'adam',
        metrics = ['accuracy']
    )

    #treinando o modelo
    hist = model.fit(
        train_images, 
        train_labels_one_hot,
        batch_size = qtd_avaliados,
        epochs = epocas,
        validation_split = validation_split
    )

    return (model, hist)

def modelo2():
    model = Sequential()

    model.add(
        Conv2D(
            filters=32,
            kernel_size=(3,3),
            activation='relu', 
            input_shape=shape_input#tipo do formato de dados esperado
        )
    )
    model.add(MaxPooling2D(pool_size=(2,2)))
    
    model.add(Flatten())
    model.add(Dense(500, activation='relu'))
    model.add(Dense(qtd_class, activation='softmax'))

    #compilando o modelo
    model.compile(
        loss = 'categorical_crossentropy',
        optimizer = 'adam',
        metrics = ['accuracy']
    )

    #treinando o modelo
    hist = model.fit(
        train_images, 
        train_labels_one_hot,
        batch_size = qtd_avaliados,
        epochs = epocas,
        validation_split = validation_split
    )

    return (model, hist)


def carregaModelo():
    #carrega o dataset
    trata = TratamentoDados()
    trata.limpa_dataset_norm()
    trata.set_dataset_path('dataset_kaggle/natural_images')
    trata.processa_labels()
    trata.processa_imagens()
    trata.processa_dados()

    (train_images, train_labels), (test_images, test_labels) = trata.get_modelos()

    #transforma os dados em array
    train_images = np.array(train_images)
    train_labels = np.array(train_labels)

    test_images = np.array(test_images)
    test_labels = np.array(test_labels)

    #normalizando o valor dos pixes
    train_images = train_images / 255
    test_images  = test_images / 255
    

    return ((train_images, train_labels), (test_images, test_labels))

#deixa o grafico gerado pelo matplot colorido
plt.style.use('fivethirtyeight')

shape_input      = (40, 40, 3)
epocas           = 20
qtd_avaliados    = 100
validation_split = 0.1#o quanto o modelo lembra dos dados em cada epoca
classification   = [
    'airplane',
    'car',
    'cat',
    'dog',
    'flower',
    'fruit',
    'motorbike',
    'person'
]
qtd_class        = len(classification)

#coloca os dados do dataset em variaves correspondentes aos dados de treino e teste
(train_images, train_labels), (test_images, test_labels) = carregaModelo()


# Ele assume que os valores da classe estavam em string e você os 
# codificará por rótulo, portanto, iniciando todas as vezes de 0 a n-classes.
train_labels_one_hot = to_categorical(train_labels)
test_labels_one_hot  = to_categorical(test_labels)


#########################
#CONFIGURAÇÃO DO MODELO
#########################

(model, hist) = modelo2()

#avalia o modelo com o dataset de teste
print(model.evaluate(test_images, test_labels_one_hot)[1])

model.save('modelo2')