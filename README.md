# PAI - Trabalho Prático sobre segmentação e classificação de imagens mamográficas

Este repositório contém o código do Trabalho Prático de Processamento e Análise de Imagens da disciplina de Ciência da Computação da PUC Minas.

## Equipe
O trabalho foi desenvolvido pelos seguintes alunos:

- Rafael Maia - 635921, Coração Eucarístico
- Jonathan Tavares - -------, Coração Eucarístico
- Giulia Chiucchi - 662103, Coração Eucarístico

## Descrição
O objetivo deste trabalho é implementar um programa que leia imagens de exames mamográficos, segmente a área da mama do fundo e possibilite o reconhecimento automático da densidade mamária, de acordo com a escala BIRADS. Para isso, é necessário realizar a segmentação automática da região da mama, deixando os elementos de fundo e anotações com valor preto (0), e, em seguida, classificar a densidade da mama, que pode ser classificada em quatro categorias: BIRADS I, BIRADS II, BIRADS III e BIRADS IV.

O dataset com as imagens para o desenvolvimento do aplicativo pode ser encontrado no seguinte link: https://www.dropbox.com/s/qt8afsmdppglahv/mamografias.zip?dl=0

## Execução
Para executar o programa, é necessário clonar este repositório. Após ter feito o clone do repositório do programa, abra o diretório do programa no terminal ou prompt de comando do seu sistema operacional. Certifique-se de que você esteja dentro da pasta raiz do programa, que deve conter o arquivo "main.py".

Uma vez dentro do diretório do programa, execute o arquivo "main.py" com o seguinte comando:

python main.py

Este comando irá executar o arquivo "main.py" usando o interpretador Python instalado em seu sistema. O programa deve começar a ser executado e, dependendo do tamanho do conjunto de dados e do poder de processamento do seu computador, pode levar alguns minutos para ser concluído.
