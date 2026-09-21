
# MindMatch — Jogo da Memória

Projeto desenvolvido para o **Checkpoint 4 da disciplina Computational Thinking using Python**, da FIAP, com o objetivo de aplicar os conceitos de programação por meio da criação de um jogo de tabuleiro utilizando matrizes bidimensionais.

O **MindMatch** é um jogo da memória com temática de séries, desenvolvido em Python, que desafia dois jogadores a encontrar pares de cartas antes que o tempo termine.

A aplicação conta com interface gráfica, placar em tempo real, cronômetro regressivo e cartas ilustradas com pôsteres de séries.

## Objetivo do projeto

Trabalhar os conceitos vistos em sala de aula como: variáveis, constantes, estruturas condicionais, estruturas de repetição, funções, sequências unidimensionais (listas, tuplas, Strings e dicionários) e listas de listas (estruturas bidimensionais).

Por meio do desenvolvimento do MindMatch, buscamos aplicar esses conhecimentos na construção de um jogo interativo em Python, utilizando uma matriz bidimensional para representar o tabuleiro e organizar as cartas.

O projeto também permite explorar a lógica de programação, o gerenciamento de estados, a interação entre jogadores e o desenvolvimento de uma interface gráfica.

## Como funciona o jogo?

O MindMatch possui um tabuleiro de **4 linhas e 6 colunas**, totalizando 24 cartas e 12 pares de séries.

Antes de iniciar, os jogadores informam seus nomes e escolhem a duração da partida, entre 5 e 10 minutos.

### Regras

1. Dois jogadores participam da partida.
2. Cada jogador seleciona duas cartas por vez.
3. Se as cartas forem iguais, o jogador ganha 1 ponto e joga novamente.
4. Se forem diferentes, as cartas são ocultadas e a vez passa para o outro jogador.
5. Os pares encontrados permanecem visíveis no tabuleiro.
6. A partida termina quando todos os pares forem encontrados ou quando o cronômetro chegar a zero.
7. Vence o jogador com a maior pontuação. Em caso de pontuações iguais, ocorre empate.

## Funcionalidades

- Tabuleiro com 24 cartas numeradas;
- Embaralhamento automático a cada partida;
- Dois jogadores com nomes personalizados;
- Placar atualizado em tempo real;
- Cronômetro configurável de 5 a 10 minutos;
- Validação da duração com mensagens em português;
- Exibição dos pôsteres das séries;
- Destaque visual para os pares encontrados;
- Bloqueio de cliques durante a verificação das cartas;
- Reinicialização da partida;
- Identificação do vencedor ou empate.

## Séries presentes no jogo

O tabuleiro utiliza 12 séries diferentes:

| Nº | Série |
|---|---|
| 1 | Stranger Things |
| 2 | The Walking Dead |
| 3 | La Casa de Papel |
| 4 | Round 6 |
| 5 | Dark |
| 6 | Lupin |
| 7 | Bridgerton |
| 8 | Black Mirror |
| 9 | The Witcher |
| 10 | One Piece |
| 11 | Arcane |
| 12 | You |

Cada série aparece duas vezes, formando os 12 pares do jogo.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Desenvolvimento da lógica do jogo |
| Tkinter | Construção da interface gráfica |
| Pillow (PIL) | Carregamento e dimensionamento dos pôsteres |
| Random | Embaralhamento das cartas |
| Time e Math | Controle do cronômetro |
| Pathlib | Localização da pasta de imagens |
| Functools | Associação das funções aos botões sem utilizar `lambda` |

## Estruturas bidimensionais

O tabuleiro é representado por uma matriz de 4 linhas e 6 colunas.

A função `criar_tabuleiro()` duplica as séries, embaralha as 24 cartas e distribui os elementos na matriz.

```python
cartas = series * 2
random.shuffle(cartas)

return [cartas[i:i + 6] for i in range(0, 24, 6)]
```

O projeto também utiliza uma segunda matriz para controlar quais cartas já foram encontradas.

```python
def criar_descobertas():
    return [[False for _ in range(6)] for _ in range(4)]
```

Cada posição começa com `False` e passa a ser `True` quando o par correspondente é encontrado.

Essa organização permite separar o conteúdo das cartas do estado de cada posição no tabuleiro.

## Principais funções

| Função | Responsabilidade |
|---|---|
| `criar_tabuleiro()` | Cria e embaralha a matriz de cartas |
| `criar_descobertas()` | Inicializa os estados das cartas |
| `verificar_par()` | Verifica se duas cartas formam um par |
| `verificar_fim()` | Identifica quando todos os pares foram encontrados |
| `resultado()` | Determina vitória ou empate |
| `clicar()` | Processa a escolha das cartas |
| `desenhar_carta()` | Atualiza a aparência das cartas |
| `atualizar_placar()` | Atualiza a pontuação dos jogadores |
| `atualizar_cronometro()` | Controla o tempo restante |
| `ocultar_erradas()` | Oculta cartas diferentes e alterna o jogador |
| `reiniciar()` | Inicia uma nova partida |
| `encerrar()` | Finaliza a partida e apresenta o resultado |

O estado do jogo é armazenado em atributos da classe `MindMatch`, sem o uso de variáveis globais para controlar a partida.

## Como executar o projeto

### Pré-requisitos

- Python 3;
- Tkinter;
- Biblioteca Pillow para exibição dos pôsteres.

O Tkinter normalmente acompanha as instalações padrão do Python para Windows.

### 1. Baixe o repositório

Faça o download do projeto pelo botão **Code → Download ZIP** no GitHub e extraia os arquivos.

### 2. Abra a pasta no VS Code

Mantenha o arquivo `MindMatch.py` e a pasta `imagens` no mesmo diretório.

```text
MindMatch/
│
├── MindMatch.py
├── README.md
│
└── imagens/
    ├── stranger_things.jpg
    ├── the_walking_dead.jpg
    ├── la_casa_de_papel.jpg
    ├── round_6.jpg
    ├── dark.jpg
    ├── lupin.jpg
    ├── bridgerton.jpg
    ├── black_mirror.jpg
    ├── the_witcher.jpg
    ├── one_piece.jpg
    ├── arcane.jpg
    └── you.jpg
```

As imagens também podem utilizar as extensões `.png` ou `.jpeg`, desde que os nomes correspondam aos identificadores utilizados no código.

### 3. Instale a biblioteca necessária

No terminal do VS Code:

```bash
python -m pip install pillow
```

### 4. Execute o jogo

```bash
python MindMatch.py
```

Informe os nomes dos jogadores, escolha a duração da partida e comece a jogar!

> **Importante:** a pasta `imagens` deve permanecer no mesmo diretório do arquivo Python para que os pôsteres sejam carregados corretamente.

## Dinâmica de apresentação

Para demonstrar o funcionamento do MindMatch na prática, a turma será dividida em dois grupos.

Cada grupo representará um jogador e poderá colaborar para memorizar as posições das cartas.

A partida terá duração de 5 minutos, permitindo demonstrar a utilização da matriz, o controle dos turnos, a pontuação e o funcionamento do cronômetro.

O grupo que encontrar mais pares será o vencedor!

## Informações acadêmicas

**Instituição:** FIAP  
**Disciplina:** Computational Thinking using Python  
**Professor:** Fernando Almeida  
**Avaliação:** Checkpoint 4 — Jogo de Tabuleiro

### Integrantes

- Isabelle Ferreira Neri Feitoza
- Marina Fernandes Gomes Mesquita
- Milena Silva Conegin


---

Desenvolvido como projeto acadêmico para aplicação prática dos conceitos de programação em Python.
