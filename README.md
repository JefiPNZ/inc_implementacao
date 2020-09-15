# Trabalho de Implementação (INC)

## Equipe

 * Andrew Vinicius da Silva Baasch
 * Jeferson Penz

## Problema

 Utilizando de Redes Neurais, desenvolver um sistema que a partir de uma entrada no formato de uma *imagem simples*, consiga identificar o *objeto* representado com base em uma lista pré-formulada (dataset).

## Dataset
 - Nome: Natural Images
 - link: https://www.kaggle.com/prasunroy/natural-images

## Técnica  

 Buscando reconhecer um objeto e as propriedades de uma imagem a ser fornecida, buscou-se elaborar uma rede neural que seja capaz de processar os diferentes pixels que compõem uma imagem e, desta forma, gerar uma lista de probabilidades sobre as quais os objetos da imagem fornecida se assemelham.

 A rede neural recebera como entrada uma imagem qualquer, inicialmente a imagem passará por um processo de normalização, este processo consite em ler as imagens e adiciona-las em vetores multidimensionais, depois os valores desses vetores são convertidas em ponto flutuante e normalizadoss em valores pequenos, e após isso o vetor é utilizado como entrada para a rede neural. Como saída a rede retornará a classe na qual ela possui maior confiança que seja aquela na qual a imagem fornecida pertence, as classes são: 0-avião, 1-carro, 2-gato, 3-cão, 4-flor, 5-fruta, 6-moto, 7-rosto.

 A técnica de validação cruzada utilizada será a Holdout, onde o dataset será dividido em dois conjuntos, um para treino e outro para teste, o conjunto de treino terá 70% dos dados do dataset, os outros 30% serão usados para teste.

## Resultados obtidos
Foram testados dois modelos com diferentes camadas, sendo eles: um com sete camadas e outro com 5. Inicialmente foi escolhido aplicar 8 épocas  e atribuído 20% de assimilação dos dados para cada época. Foi constatado que 8 não era um valor suficientemente bom, já que apenas na oitava época o modelo começava a melhorar (além de que a quantidade de dados que o modelo lembrava estava influenciando bastante). Desta forma, optamos por atribuir 20 épocas para teste com 10% de assimilação de dados por época. Ambos os modelos testados se saíram melhor com a aplicação de 10% de assimilação dos dados por época, mas em todos os cenários, o que apresentou melhores resultados foi o de 5 camadas.

## Instruções de uso

 Para criar o modelo acesse o arquivo "rede_neural.py", no método "carregaModelo" passe o caminho relativo para a pasta onde se encontra o dataset. ajuste as seguintes variaveis:
- shape_input: O formato de dados de entrada da rede.
- epocas: A quantidade de épocas que se deseja que sejam executadas.
- qtd_avaliados: A quantidade de dados que é verificada por vez.
- validation_split: O quanto o modelo lembra dos dados em cada epoca
- classification: As classes contidas no modelo.
- qtd_class: Quantidade de classes que o modelo possui.

 Na última linha passe o nome desejado do modelo. O modelo sera salvo na pasta raiz. Após ter gerado o modelo vá no aquivo "main.py" e na linha 27 passe o nome do modelo gerado.

 
