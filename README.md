<h1 align="center">MindMatch — Jogo da Memória</h1>

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/><img src="https://img.shields.io/badge/TKINTER-008080?style=for-the-badge&logoColor=white" alt="Tkinter"/><img src="https://img.shields.io/badge/PILLOW-FFCA28?style=for-the-badge&logoColor=black" alt="Pillow"/><img src="https://img.shields.io/badge/FIAP-ED145B?style=for-the-badge&logoColor=white" alt="FIAP"/><img src="https://img.shields.io/badge/CHECKPOINT_4-202020?style=for-the-badge&logoColor=white" alt="Checkpoint 4"/>
</p>

## Sobre o projeto

O **MindMatch** é um jogo da memória desenvolvido em **Python**, com interface gráfica e temática de séries.

O projeto foi criado para o **Checkpoint 4 da disciplina de Pensamento Computacional da FIAP**, com o objetivo de aplicar conceitos de programação estudados em aula, especialmente o uso de listas e matrizes bidimensionais.

Dois jogadores disputam uma partida para encontrar pares de cartas com imagens de séries. Cada par encontrado vale um ponto. A partida termina quando todos os pares são descobertos ou quando o tempo se esgota.

## Funcionalidades

- Tabuleiro com **24 cartas**, distribuídas em uma matriz de **4 linhas e 6 colunas**.
- **12 pares** com temática de séries.
- Embaralhamento das cartas a cada partida.
- Partidas para dois jogadores, com nomes e placar.
- O jogador que acerta um par ganha um ponto e continua jogando; em caso de erro, a vez passa para o outro jogador.
- Cronômetro configurável de **5 a 10 minutos**.
- Resultado final com vencedor ou empate.
- Botão para reiniciar a partida.

## Conceitos de Python utilizados

- Variáveis e estruturas condicionais (`if` e `else`).
- Estruturas de repetição (`for` e `while`).
- Funções com parâmetros e retornos.
- Listas, tuplas, strings e dicionários.
- Matrizes bidimensionais (listas de listas).
- Tratamento de exceções com `try` e `except`.
- Importação e utilização de bibliotecas Python.

A lógica do jogo é organizada em **funções**, sem classes criadas no projeto e sem expressões `lambda`. As matrizes representam o tabuleiro e controlam quais cartas já foram descobertas.

## Tecnologias e bibliotecas

| Tecnologia | Utilização |
| --- | --- |
| **Python** | Linguagem de programação do projeto. |
| **Tkinter** | Interface gráfica, botões e janelas de diálogo. |
| **Pillow** | Carregamento e ajuste das imagens das cartas. |
| `random` | Embaralhamento das cartas. |
| `math` e `time` | Controle do cronômetro. |
| `functools.partial` | Associação dos botões às funções de clique. |
| `pathlib` | Localização da pasta de imagens. |

**Observação:** Pillow é opcional. Se não estiver instalada, ou se as imagens não estiverem disponíveis, o jogo pode mostrar os nomes das séries no lugar das imagens.

## Como executar

É recomendado usar **Python 3.12 ou superior**. O Tkinter deve estar disponível na instalação do Python.

### 1. Clonar o repositório

```bash
git clone https://github.com/isabelleferreiraa/jogo-da-memoria.git
```

### 2. Entrar na pasta

```bash
cd jogo-da-memoria
```

### 3. Instalar Pillow para visualizar as imagens

```bash
python -m pip install Pillow
```

### 4. Executar o jogo

```bash
python MindMatch.py
```

No Windows, se o comando `python` não estiver disponível, tente:

```bash
py MindMatch.py
```

## Regras do jogo

1. Os dois jogadores informam seus nomes.
2. É definida a duração da partida, de 5 a 10 minutos.
3. As 24 cartas são embaralhadas e distribuídas no tabuleiro.
4. O jogador da vez seleciona duas cartas.
5. Se as cartas formarem um par, ele recebe um ponto e continua jogando.
6. Se as cartas forem diferentes, elas são ocultadas novamente e a vez passa ao outro jogador.
7. A partida termina quando os 12 pares forem encontrados ou quando o cronômetro chegar a zero.
8. Vence quem tiver mais pontos; se as pontuações forem iguais, há empate.

## Estrutura do repositório

```text
jogo-da-memoria/
├── MindMatch.py
├── README.md
├── Apresentacao dos Slides - MindMatch.pdf
└── imagens/
    ├── arcane.jpeg
    ├── black_mirror.jpeg
    ├── bridgerton.jpeg
    ├── dark.jpeg
    ├── la_casa_de_papel.jpeg
    ├── lupin.jpeg
    ├── one_piece.jpeg
    ├── round_6.jpeg
    ├── stranger_things.jpeg
    ├── the_walking_dead.jpeg
    ├── the_witcher.jpeg
    └── you.jpeg
```

## Integrantes

**FIAP — Checkpoint 4 de Pensamento Computacional**

- Isabelle Ferreira Neri Feitoza — RM573507
- Marina Fernandes Gomes Mesquita — RM571265
- Milena Silva Conegin — RM568923

## Apresentação

[Ver a apresentação do MindMatch em PDF](./Apresentacao%20dos%20Slides%20-%20MindMatch.pdf)
