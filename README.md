# Trabalho de Implementação (INC)

## Equipe

 * Andrew Vinicius da Silva Baasch
 * Jeferson Penz

## Problema
 Utilizando de Redes Neurais, desenvolver um sistema que dado uma entrada no formato de uma *imagem simples*, o sistema consiga identificar o *objeto* representado a partir de uma lista pré-formulada vinda do dataset.

## Dataset
 Nome: Natural Images
 link: https://www.kaggle.com/prasunroy/natural-images

## Técnica  
 Dado o objetivo de reconhecer um objeto e as propriedades de uma imagem a ser fornecida, busca-se elaborar uma rede neural que seja capaz de processar os diferentes pixeis que compoem uma imagem e desta gerar uma lista de probabilidades sobre a quais objetos a imagem fornecida se assemelha.

 A rede neural recebera como entrada uma imagem qualquer, inicialmente a imagem passará por um processo de normalização, este processo consite em alterar as cores da imagem para preto e branco e redimensiona-la para o tamanho que a rede espera. Como saída a rede retornará a classe na qual ela possui maior confiança que seja aquela na qual a imagem fornecida pertence, as classes são: 0-avião, 1-carro, 2-gato, 3-cão, 4-flor, 5-fruta, 6-moto, 7-pessoa.

 A técnica de validação cruzada utilizada será a Holdout, onde o dataset será dividido em dois conjuntos, um para treino e outro para teste, o conjunto de treino terá 70% dos dados do dataset, os outros 30% serão usados para teste.
