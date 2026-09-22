# ==============================================================================
# MINDMATCH — JOGO DA MEMÓRIA COM TEMÁTICA DA NETFLIX
# ==============================================================================
# Integrantes:
# Isabelle Ferreira Neri Feitoza | RM573507
# Marina Fernandes Gomes Mesquita | RM571265
# Milena Silva Conegin | RM568923
# ==============================================================================
# Projeto em Python:
# - Tabuleiro formado por uma matriz 4 x 6 (24 cartas / 12 pares).
# - Dois jogadores alternam turnos; cada par correto vale 1 ponto.
# - A partida termina quando todos os pares forem encontrados OU o tempo escolhido (5–10 min).
# ==============================================================================

import random
import math
import time
import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import messagebox, simpledialog

# Tenta carregar a biblioteca Pillow (PIL) para suporte a imagens. (pip install Pillow)
# Se não estiver instalada, o jogo rodará normalmente no modo apenas texto.
try:
    from PIL import Image, ImageOps, ImageTk
except ImportError:
    Image = ImageOps = ImageTk = None

# ==============================================================================

#Retorna uma matriz 4 x 6 de séries embaralhadas (24 cartas, 12 pares).
def criar_tabuleiro():
    series = [
        ("Stranger Things", "stranger_things"),
        ("The Walking Dead", "the_walking_dead"),
        ("La Casa de Papel", "la_casa_de_papel"),
        ("Round 6", "round_6"),
        ("Dark", "dark"),
        ("Lupin", "lupin"),
        ("Bridgerton", "bridgerton"),
        ("Black Mirror", "black_mirror"),
        ("The Witcher", "the_witcher"),
        ("One Piece", "one_piece"),
        ("Arcane", "arcane"),
        ("You", "you"),
    ]
    # Duplica a lista para formar os pares e embaralha a ordem
    cartas = series * 2
    random.shuffle(cartas)

    # Converte a lista plana de 24 itens em uma matriz de 4 linhas por 6 colunas
    return [cartas[i:i + 6] for i in range(0, 24, 6)]

#Retorna outra matriz 4x6, começando com False em todas as posições, para rastrear cartas reveladas.
def criar_descobertas():
    return [[False for _ in range(6)] for _ in range(4)]

#Recebe a matriz e duas coordenadas; retorna True se as séries coincidirem.
def verificar_par(tabuleiro, primeira, segunda):
    l1, c1 = primeira
    l2, c2 = segunda
    return tabuleiro[l1][c1][1] == tabuleiro[l2][c2][1]

#Verifica se todas as posições da matriz já foram descobertas.
def verificar_fim(descobertas):
    return all(all(linha) for linha in descobertas)

#Recebe nomes/placares e devolve texto de vitória ou empate.
def resultado(nomes, pontos):
    if pontos[0] == pontos[1]:
        return f"Empate! {nomes[0]} e {nomes[1]} fizeram {pontos[0]} pontos."
    vencedor = 0 if pontos[0] > pontos[1] else 1
    return f"{nomes[vencedor]} venceu por {pontos[vencedor]} a {pontos[1 - vencedor]}!"


def pedir_duracao(parent, inicial=5):
    """Solicita de 5 a 10 minutos e apresenta todos os avisos em português.

    Retorna None quando o jogador cancela, mantendo o comportamento anterior.
    """
    while True:
        resposta = simpledialog.askstring(
            "Duração da partida",
            "Quantos minutos vocês querem jogar? (5 a 10)",
            parent=parent,
            initialvalue=str(inicial),
        )
        if resposta is None:
            return None
        try:
            minutos = int(resposta)
        except ValueError:
            minutos = None
        if minutos is not None and 5 <= minutos <= 10:
            return minutos
        messagebox.showwarning(
            "Tempo inválido",
            "Escolha um número inteiro de 5 a 10 minutos.",
            parent=parent,
        )


# ------------------------------------------------------------------------------
# INTERFACE GRÁFICA E CONTROLE DA PARTIDA COM FUNÇÕES
# ------------------------------------------------------------------------------

# Cria a janela e guarda os dados da partida em um dicionário.
def iniciar_jogo(janela):
    estado = {"janela": janela}
    estado["janela"].title("MindMatch — Jogo da Memória")
    estado["janela"].configure(bg="#141414")
    estado["janela"].resizable(False, False)

    # Esconde a janela principal para exibir os diálogos de configuração inicial
    estado["janela"].withdraw()

    nome1 = simpledialog.askstring("Jogador 1", "Nome do jogador 1:", parent=janela)
    nome2 = simpledialog.askstring("Jogador 2", "Nome do jogador 2:", parent=janela)
    estado["nomes"] = [
        nome1.strip() if nome1 and nome1.strip() else "Jogador 1",
        nome2.strip() if nome2 and nome2.strip() else "Jogador 2",
    ]

    #Duração da partida
    duracao = pedir_duracao(janela, inicial=5)

    estado["duracao_minutos"] = duracao if duracao is not None else 5

    # Exibe a janela principal após a coleta das configurações
    estado["janela"].deiconify()

    # Variáveis de controle de estado do jogo
    estado["pasta_imagens"] = Path(__file__).resolve().parent / "imagens"
    estado["fotos"] = carregar_imagens(estado)
    estado["tabuleiro"] = []
    estado["descobertas"] = []
    estado["botoes"] = []
    estado["selecionadas"] = []
    estado["pontos"] = [0, 0]
    estado["jogador_atual"] = 0
    estado["bloqueado"] = False    # Bloqueia cliques adicionais durante validações
    estado["rodada_id"] = 0        # Identificador único para sincronização do tempo
    estado["tempo_limite"] = 0
    estado["cronometro_ativo"] = False
    estado["temporizador_id"] = None
    estado["partida_encerrada"] = False

    # --- CONSTRUÇÃO DA INTERFACE VISUAL ---
    # Cabeçalho da aplicação
    tk.Label(
        janela,
        text="MINDMATCH",
        font=("Arial", 29, "bold"),
        fg="#E50914",
        bg="#141414",
    ).pack(pady=(16, 0))
    tk.Label(
        janela,
        text="Encontre os 12 pares de séries!",
        font=("Arial", 11),
        fg="#CCCCCC",
        bg="#141414",
    ).pack(pady=(0, 10))

    # Painel Superior (Placar e Cronômetro)
    painel_topo = tk.Frame(janela, bg="#141414")
    painel_topo.pack(pady=(2, 8))

    cor_painel = "#1B2128"
    borda_painel = "#2F3A46"

    # Quadros informativos: Jogador 1, Cronômetro e Jogador 2
    estado["painel_j1"] = tk.Frame(
        painel_topo,
        bg=cor_painel,
        highlightbackground=borda_painel,
        highlightthickness=1,
        width=145,
        height=72,
    )
    estado["painel_j1"].grid(row=0, column=0, padx=6)
    estado["painel_j1"].grid_propagate(False)

    estado["painel_tempo"] = tk.Frame(
        painel_topo,
        bg=cor_painel,
        highlightbackground="#B20710",
        highlightthickness=1,
        width=145,
        height=72,
    )
    estado["painel_tempo"].grid(row=0, column=1, padx=6)
    estado["painel_tempo"].grid_propagate(False)

    estado["painel_j2"] = tk.Frame(
        painel_topo,
        bg=cor_painel,
        highlightbackground=borda_painel,
        highlightthickness=1,
        width=145,
        height=72,
    )
    estado["painel_j2"].grid(row=0, column=2, padx=6)
    estado["painel_j2"].grid_propagate(False)

    # Conteúdo do painel do jogador 1.
    tk.Label(
        estado["painel_j1"],
        text="Jogador 1",
        font=("Arial", 8),
        fg="#9AA6B2",
        bg=cor_painel,
    ).place(x=8, y=6)
    estado["nome_j1"] = tk.Label(
        estado["painel_j1"],
        text=estado["nomes"][0],
        font=("Arial", 12, "bold"),
        fg="white",
        bg=cor_painel,
        anchor="w",
    )
    estado["nome_j1"].place(x=8, y=31)
    estado["pontos_j1"] = tk.Label(
        estado["painel_j1"],
        text="0",
        font=("Arial", 18, "bold"),
        fg="#E50914",
        bg=cor_painel,
    )
    estado["pontos_j1"].place(x=110, y=24)

    # Conteúdo do painel central de tempo.
    tk.Label(
        estado["painel_tempo"],
        text="Tempo",
        font=("Arial", 8),
        fg="#9AA6B2",
        bg=cor_painel,
    ).place(relx=0.5, y=6, anchor="n")
    estado["cronometro"] = tk.Label(
        estado["painel_tempo"],
        text="05:00",
        font=("Arial", 21, "bold"),
        fg="#F5C518",
        bg=cor_painel,
    )
    estado["cronometro"].place(relx=0.5, y=26, anchor="n")

    # Conteúdo do painel do jogador 2.
    tk.Label(
        estado["painel_j2"],
        text="Jogador 2",
        font=("Arial", 8),
        fg="#9AA6B2",
        bg=cor_painel,
    ).place(x=8, y=6)
    estado["nome_j2"] = tk.Label(
        estado["painel_j2"],
        text=estado["nomes"][1],
        font=("Arial", 12, "bold"),
        fg="white",
        bg=cor_painel,
        anchor="w",
    )
    estado["nome_j2"].place(x=8, y=31)
    estado["pontos_j2"] = tk.Label(
        estado["painel_j2"],
        text="0",
        font=("Arial", 18, "bold"),
        fg="#E50914",
        bg=cor_painel,
    )
    estado["pontos_j2"].place(x=110, y=24)

    # Status logo abaixo da tabela.
    estado["status"] = tk.Label(
        janela,
        text="",
        font=("Arial", 11, "bold"),
        fg="#F5C518",
        bg="#141414",
    )
    estado["status"].pack(pady=(0, 10))

    # Tabuleiro
    grade = tk.Frame(janela, bg="#141414")
    grade.pack(padx=16)
    for linha in range(4):
        linha_botoes = []
        for coluna in range(6):
            caixa = tk.Frame(grade, width=122, height=120, bg="#141414")
            caixa.grid(row=linha, column=coluna, padx=4, pady=4)
            caixa.grid_propagate(False)
            botao = tk.Button(
                caixa,
                font=("Arial", 11, "bold"),
                bd=0,
                relief="flat",
                wraplength=108,
                cursor="hand2",
                command=partial(clicar, estado, linha, coluna),
            )
            botao.place(relx=0, rely=0, relwidth=1, relheight=1)
            linha_botoes.append(botao)
        estado["botoes"].append(linha_botoes)

    # Botão para Reiniciar
    tk.Button(
        janela,
        text="REINICIAR PARTIDA",
        font=("Arial", 10, "bold"),
        fg="white",
        bg="#B20710",
        activebackground="#E50914",
        bd=0,
        padx=15,
        pady=9,
        cursor="hand2",
        command=partial(reiniciar, estado, escolher_tempo=True),
    ).pack(pady=(11, 8))

    reiniciar(estado)
    return estado


def carregar_imagens(estado):
    fotos = {}
    if Image is None or not estado["pasta_imagens"].is_dir():
        return fotos

    nomes = [
        "stranger_things", "the_walking_dead", "la_casa_de_papel", "round_6",
        "dark", "lupin", "bridgerton", "black_mirror",
        "the_witcher", "one_piece", "arcane", "you"
    ]
    for nome in nomes:
        for extensao in (".png", ".jpg", ".jpeg"):
            caminho = estado["pasta_imagens"] / (nome + extensao)
            if caminho.is_file():
                try:
                    with Image.open(caminho) as original:
                        imagem = ImageOps.contain(original.convert("RGB"), (108, 108))
                    fotos[nome] = ImageTk.PhotoImage(imagem)
                    break
                except (OSError, ValueError):
                    pass
    return fotos


def reiniciar(estado, escolher_tempo=False):
    if escolher_tempo:
        duracao = pedir_duracao(estado["janela"], inicial=estado["duracao_minutos"])
        if duracao is None:
            return
        estado["duracao_minutos"] = duracao

    # Cancela temporizadores anteriores ativos
    if estado["temporizador_id"] is not None:
        estado["janela"].after_cancel(estado["temporizador_id"])
        estado["temporizador_id"] = None

    estado["rodada_id"] += 1
    estado["partida_encerrada"] = False
    estado["tabuleiro"] = criar_tabuleiro()
    estado["descobertas"] = criar_descobertas()
    estado["selecionadas"] = []
    estado["pontos"] = [0, 0]
    estado["jogador_atual"] = 0
    estado["bloqueado"] = False

    for linha in range(4):
        for coluna in range(6):
            desenhar_carta(estado, linha, coluna)

    # Reseta o visual de todas as cartas
    atualizar_placar(estado)
    estado["status"].config(text=f"Vez de {estado["nomes"][estado["jogador_atual"]]}")

    # Configura a nova contagem de tempo
    estado["tempo_limite"] = time.monotonic() + estado["duracao_minutos"] * 60
    estado["cronometro_ativo"] = True
    atualizar_cronometro(estado, estado["rodada_id"])


def atualizar_cronometro(estado, rodada):
    if rodada != estado["rodada_id"] or not estado["cronometro_ativo"]:
        return

    estado["temporizador_id"] = None
    segundos = max(0, math.ceil(estado["tempo_limite"] - time.monotonic()))
    minutos, segundos_restantes = divmod(segundos, 60)
    estado["cronometro"].config(
        text=f"{minutos:02d}:{segundos_restantes:02d}",
        fg="#E50914" if segundos <= 30 else "#F5C518",
    )

    # Encerramento por estouro do tempo
    if segundos == 0:
        estado["cronometro_ativo"] = False
        estado["bloqueado"] = True
        escolhidas = estado["selecionadas"][:]
        estado["selecionadas"] = []
        for linha, coluna in escolhidas:
            desenhar_carta(estado, linha, coluna)
        estado["status"].config(text="Tempo esgotado! Fim da partida.")
        encerrar(estado, rodada, por_tempo=True)
        return

    # Loop de atualização do relógio a cada 200 milissegundos
    estado["temporizador_id"] = estado["janela"].after(200, atualizar_cronometro, estado, rodada)


def atualizar_placar(estado):
    estado["nome_j1"].config(text=estado["nomes"][0])
    estado["nome_j2"].config(text=estado["nomes"][1])
    estado["pontos_j1"].config(text=str(estado["pontos"][0]))
    estado["pontos_j2"].config(text=str(estado["pontos"][1]))


def desenhar_carta(estado, linha, coluna):
    botao = estado["botoes"][linha][coluna]
    posicao = (linha, coluna)
    aberta = estado["descobertas"][linha][coluna] or posicao in estado["selecionadas"]

    # Carta Virada para Baixo
    if not aberta:
        botao.config(
            text=str(linha * 6 + coluna + 1),
            image="",
            bg="#B20710",
            fg="white",
            activebackground="#E50914",
            font=("Arial", 26, "bold"),
        )
        return

    # Carta Revelada (com imagem ou apenas texto)
    nome, arquivo = estado["tabuleiro"][linha][coluna]
    cor = "#155E49" if estado["descobertas"][linha][coluna] else "#303030"
    foto = estado["fotos"].get(arquivo)
    if foto is not None:
        botao.config(
            image=foto,
            text="",
            compound="top",
            bg=cor,
            fg="white",
            font=("Arial", 9, "bold"),
        )
    else:
        botao.config(
            image="",
            text=nome,
            bg=cor,
            fg="white",
            font=("Arial", 11, "bold"),
        )


def clicar(estado, linha, coluna):
    posicao = (linha, coluna)

    # Ignora cliques em cartas já abertas ou durante bloqueio de turno
    if (estado["bloqueado"] or estado["descobertas"][linha][coluna]
            or posicao in estado["selecionadas"]):
        return

    estado["selecionadas"].append(posicao)
    desenhar_carta(estado, linha, coluna)

    # Aguarda a seleção do segundo par
    if len(estado["selecionadas"]) < 2:
        return

    estado["bloqueado"] = True
    primeira, segunda = estado["selecionadas"]

    # Processamento de Par Encontrado
    if verificar_par(estado["tabuleiro"], primeira, segunda):
        for l, c in estado["selecionadas"]:
            estado["descobertas"][l][c] = True
            desenhar_carta(estado, l, c)

        estado["pontos"][estado["jogador_atual"]] += 1
        atualizar_placar(estado)
        estado["selecionadas"] = []

        # Checa se o jogo chegou ao fim por conclusão do tabuleiro
        if verificar_fim(estado["descobertas"]):
            estado["status"].config(text="Todos os pares encontrados!")
            estado["cronometro_ativo"] = False
            if estado["temporizador_id"] is not None:
                estado["janela"].after_cancel(estado["temporizador_id"])
                estado["temporizador_id"] = None
            estado["janela"].after(500, encerrar, estado, estado["rodada_id"])
        else:
            estado["status"].config(text=f"Vez de {estado["nomes"][estado["jogador_atual"]]}")
            estado["bloqueado"] = False

    # Processamento de Erro (Par Incorreto)
    else:
        estado["status"].config(text=f"Vez de {estado["nomes"][1 - estado["jogador_atual"]]}")
        estado["janela"].after(1300, ocultar_erradas, estado, estado["rodada_id"])


def ocultar_erradas(estado, rodada):
    if rodada != estado["rodada_id"] or estado["partida_encerrada"]:
        return

    escolhidas = estado["selecionadas"][:]
    estado["selecionadas"] = []
    for linha, coluna in escolhidas:
        desenhar_carta(estado, linha, coluna)

    # Alterna o turno entre jogador 0 e jogador 1
    estado["jogador_atual"] = 1 - estado["jogador_atual"]
    estado["status"].config(text=f"Vez de {estado["nomes"][estado["jogador_atual"]]}")
    estado["bloqueado"] = False


def encerrar(estado, rodada, por_tempo=False):
    if rodada != estado["rodada_id"] or estado["partida_encerrada"]:
        return

    estado["partida_encerrada"] = True
    estado["cronometro_ativo"] = False
    estado["bloqueado"] = True
    mensagem = resultado(estado["nomes"], estado["pontos"])
    if por_tempo:
        mensagem = "O tempo acabou!\n\n" + mensagem
    else:
        mensagem = "Todos os pares foram encontrados!\n\n" + mensagem
    messagebox.showinfo("Fim de jogo", mensagem, parent=estado["janela"])



# ------------------------------------------------------------------------------
# PONTO DE ENTRADA DO PROGRAMA
# ------------------------------------------------------------------------------        

#Inicializa a aplicação Tkinter; não guarda estado em variáveis globais.
def main():
    janela = tk.Tk()
    iniciar_jogo(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
