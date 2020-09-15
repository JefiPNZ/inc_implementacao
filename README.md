# Trabalho de Implementação (INC)

## Equipe

 * Andrew Vinicius da Silva Baasch
 * Jeferson Penz

## Problema
 Utilizando de Redes Neurais, desenvolver um sistema que dado uma entrada no formato de uma *imagem simples*, o sistema consiga identificar o *objeto* representado a partir de uma lista pré-formulada vinda do dataset.

## Dataset
 - Nome: Natural Images
 - link: https://www.kaggle.com/prasunroy/natural-images

## Técnica  
 Dado o objetivo de reconhecer um objeto e as propriedades de uma imagem a ser fornecida, busca-se elaborar uma rede neural que seja capaz de processar os diferentes pixeis que compoem uma imagem e desta gerar uma lista de probabilidades sobre a quais objetos a imagem fornecida se assemelha.

 A rede neural recebera como entrada uma imagem qualquer, inicialmente a imagem passará por um processo de normalização, este processo consite em ler as imagens e adiciona-las em vetores multidimensionais, depois os valores desses vetores são convertidas em ponto flutuante e normalizadoss em valores pequenos, e após isso o vetor é utilizado como entrada para a rede neural. Como saída a rede retornará a classe na qual ela possui maior confiança que seja aquela na qual a imagem fornecida pertence, as classes são: 0-avião, 1-carro, 2-gato, 3-cão, 4-flor, 5-fruta, 6-moto, 7-rosto.

 A técnica de validação cruzada utilizada será a Holdout, onde o dataset será dividido em dois conjuntos, um para treino e outro para teste, o conjunto de treino terá 70% dos dados do dataset, os outros 30% serão usados para teste.

## Resultados obtidos
Foram testados dois modelos com diferentes camadas. Um com sete camadas e um com 5. inicialmente testamos com 8 epocas e definimos que o modelo lembraria de 20% dos dados de cada época, vimos que eram poucas épocas, só na oitava época que o modelo começava a melhorar, e a quantidade de dados que o modelo lembrava estava influenciando bastante. Mudamos para 20 épocas e definimos que o modelo lembraria de 10% dos dados de cada epoca, ambos os modelos testados se sairam melhor com esses parametros. Em todos os casos o modelo com 5 camadas foi o melhor.

## Instruções de uso

 Para criar o modelo acesse o arquivo "rede_neural.py", no método "carregaModelo" passe o caminho relativo para a pasta onde se encontra o dataset. ajuste as seguintes variaveis:
- shape_input: O formato de dados de entrada da rede.
- epocas: A quantidade de épocas que se deseja que sejam executadas.
- qtd_avaliados: A quantidade de dados que é verificada por vez.
- validation_split: O quanto o modelo lembra dos dados em cada epoca
- classification: As classes contidas no modelo.
- qtd_class: Quantidade de classes que o modelo possui.

 Na última linha passe o nome desejado do modelo. O modelo sera salvo na pasta raiz. Após ter gerado o modelo vá no aquivo "main.py" e na linha 27 passe o nome do modelo gerado.

 
