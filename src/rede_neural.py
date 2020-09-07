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


# nome_classe = [
#             'airplane', 'car', 'cat', 'dog', 'motorbike', 'person'
#             ]

# model = tf.keras.models.load_model('modelo_teste')

# img = gm.abri_imagem('carro2.jpg')
# img = gm.redimenciona_imagem(img)

# predictions_single = model.predict(np.array([gm.redimenciona_imagem(img)]))

# print(predictions_single)

# n = np.argmax(predictions_single[0])
# print(f'{n} {nome_classe[n]}')
# sys.exit(0)


#deixa o grafico gerado pelo matplot colorido
plt.style.use('fivethirtyeight')

#carrega o dataset
trata = TratamentoDados()
trata.limpa_dataset_norm()
trata.set_dataset_path('dataset_kaggle/natural_images')
trata.processa_labels()
trata.processa_imagens()
trata.processa_dados()

#coloca os dados do dataset em variaves correspondentes aos dados de treino e teste
(train_images, train_labels), (test_images, test_labels) = trata.get_modelos()

# for i, value in enumerate(train_labels):
#     train_labels[i] = np.array(value)

# sys.exit(0)

#transforma os dados em array
train_images = np.array(train_images)
train_labels = np.array(train_labels)

test_images = np.array(test_images)
test_labels = np.array(test_labels)

#normalizando o valor dos pixes
train_images = train_images / 255
test_images  = test_images / 255

#printa a forma do array
print(train_images[0].shape)


#verificando a primeira imagem do array
index = 1
plt.imshow(train_images[index])
plt.show()

#label da imagem
print(f'label da imagem:{train_labels[index]}')

#classificacao da imagem
classification = trata.get_class_names()
#image class
print(f'classe da imagem:{classification[train_labels[index]]}')

#Ele assume que os valores da classe estavam em string e você os 
# codificará por rótulo, portanto, iniciando todas as vezes de 0 a n-classes.
train_labels_one_hot = to_categorical(train_labels)
test_labels_one_hot  = to_categorical(test_labels)

# #mostra no console os labels
# print(train_labels)

#########################
#CONFIGURAÇÃO DO MODELO
#########################

#arquitetura do modelo
#O modelo sequential agrupa um conjunto de camadas de forma linear
model = Sequential()

#adiciona a primeira camada da rede
#Camada de convolução 2D (convolução espacial sobre imagens).
model.add(
    Conv2D(
        filters=64,
        kernel_size=(5,5),
        activation='relu', 
        input_shape=(40, 40, 3)#tipo do formato de dados esperado
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

#adiciona camada de saida
model.add(Dropout(0.5))

#adicionando uma camada com 250 neuronios
model.add(Dense(400, activation='relu'))

#adicionando uma camada com 10 neuronios, para as 10 classes diferentes de arquivos
model.add(Dense(7, activation='softmax'))

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
    batch_size = 256,
    epochs = 8,
    validation_split = 0.2
)

#avalia o modelo com o dataset de teste
print(model.evaluate(test_images, test_labels_one_hot)[1])

#visualização da precisão do modelo
plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Precisao do modelo')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc="upper right")
plt.show()

#visualização da perda do modelo
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Perda do modelo')
plt.ylabel('loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc="upper right")
plt.show()

#exemplo
imagem = gm.abri_imagem('cao.jpg')

#verificando a predição do modelo
predictions = model.predict(np.array([gm.redimenciona_imagem(imagem)]))
print(predictions)


#predicoes
list_index = [0,1,2,3,4,5,6]
x = predictions

for i in range(7):
    for j in range(7):
        if x[0][list_index[i]] > x[0][list_index[j]]:
           temp = list_index[i]
           list_index[i] = list_index[j]
           list_index[j] = temp

print(list_index)

for i in range(5):
    print(classification[list_index[i]], ':', round(predictions[0][list_index[i]] * 100, 2), '%')

model.save('modelo_teste_sem_flor')
para = 1