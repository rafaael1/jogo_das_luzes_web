X = "\033[7;31mX\033[m"
O = "\033[1;33mO\033[m"


def instrucoes():
    print(
        "<---------------------------------- \033[1;30;43mJogo das Luzes\033[m ---------------------------------->")
    print()
    print(
        """   O objetivo do jogo das luzes é transformar todas as peças vermelhas em amarelas, 
              com o menor números de jogadas.

              \033[1;31;4mX\033[m -> Luz \033[1;37;4mapagada\033[m
              \033[1;33;4mO\033[m -> Luz \033[1;33;4macesa\033[m
        """
    )
    champion = openFile()[0].rstrip().rsplit(',')
    print("   " + "-"*80)
    print(
        f"          \U0001F3C6 \U0001F3C6 \U0001F3C6   \033[1;37;41m  Champion --->  {champion[0]} - {champion[1]} tentativas   \033[m \U0001F3C6 \U0001F3C6 \U0001F3C6")
    print("   " + "-"*80)


def openFile():
    # 1. Ler txt com o ranking e número de jogadas utilizadas para ganhar
    with open("ranking_jogo.txt", mode="r", encoding="utf-8") as f:
        linhas = f.readlines()

    return linhas


def printRanking():
    linhas = openFile()

    print("\t\t########   \U0001F947  \033[1;32;45mRanking de jogadores\033[m       ########", end="\n\n")
    for ind, linha in enumerate(linhas):
        print(f"\t\t\t   {ind+1}. {linha.strip()}")


def clearScreen():
    print("\x1b[2J\x1b[1;1H")


def menuGame():
    # 2. Menu perguntando se o jogador quer jogar ou sair ou ver o ranking
    print("\n\t\t\t********   Deseja Jogar?   ********\n")
    print("\t\t|\t        \033[1;35m[ 1 ] - Jogar   \033[m\U0001F3B2    \t\t|")
    print("\t\t|\t        \033[1;32m[ 2 ] - Ranking \033[m\U0001F3C5     \t\t|")
    print("\t\t|\t        \033[1;37m[ 0 ] - Sair    \033[m\U0001F91D     \t\t|\n")

    escolha = input("\n\t\t\t     \U0001F449  Sua Escolha: ")
    escolha = int(escolha) if escolha.isdigit() else -1

    # 3. Número de jogadas o jogador quer para tentar ganhar o jogo
    if escolha == 1:
        jogadas = int(input("Qual o número de jogadas que você quer? "))
        return jogadas
    elif escolha == 2:
        clearScreen()
        printRanking()
        return -2
    elif escolha == 0:
        return 0
    else:
        print("\nEntre com um valor válido!")
        return -1


# Verifica se o jogo acabou (se não existe mais 'X')
def validacao():
    return X in jogo[0] or X in jogo[1] or X in jogo[2] or X in jogo[3] or X in jogo[4]


def validaEntrada():
    while True:  # Loop para verificar se está correto os valores inseridos
        linhaEscolhida = input("Qual linha deseja escolher? ")
        linhaEscolhida = int(
            linhaEscolhida) if linhaEscolhida.isdigit() else -3
        colunaEscolhida = input("Qual coluna deseja escolher? ")
        colunaEscolhida = int(
            colunaEscolhida) if colunaEscolhida.isdigit() else -3

        if (
            linhaEscolhida >= 1
            and linhaEscolhida <= 5
            and colunaEscolhida >= 1
            and colunaEscolhida <= 5
        ):
            return linhaEscolhida, colunaEscolhida
        else:
            print("\nValores incorretos! Insira novamente os valores\n")


def verificaBorda(linha, coluna) -> list:

    if linha == 1:
        if coluna == 1:
            return [(linha, coluna), (linha + 1, coluna), (linha, coluna + 1)]
        elif coluna == 5:
            return [(linha, coluna), (linha + 1, coluna), (linha, coluna - 1)]
        else:
            return [
                (linha, coluna),
                (linha + 1, coluna),
                (linha, coluna + 1),
                (linha, coluna - 1),
            ]

    elif linha == 5:
        if coluna == 1:
            return [(linha, coluna), (linha - 1, coluna), (linha, coluna + 1)]
        elif coluna == 5:
            return [(linha, coluna), (linha - 1, coluna), (linha, coluna - 1)]
        else:
            return [
                (linha, coluna),
                (linha - 1, coluna),
                (linha, coluna + 1),
                (linha, coluna - 1),
            ]

    elif coluna == 1:
        return [
            (linha, coluna),
            (linha - 1, coluna),
            (linha, coluna + 1),
            (linha + 1, coluna),
        ]

    elif coluna == 5:
        return [
            (linha, coluna),
            (linha - 1, coluna),
            (linha, coluna - 1),
            (linha + 1, coluna),
        ]

    else:  # Retorna 5 valores
        return [
            (linha, coluna),
            (linha - 1, coluna),
            (linha, coluna - 1),
            (linha + 1, coluna),
            (linha, coluna + 1),
        ]


def aplicaJogada(vetorJogadas):
    for valor in vetorJogadas:
        if jogo[valor[0] - 1][valor[1] - 1] == X:
            jogo[valor[0] - 1][valor[1] - 1] = O
        else:
            jogo[valor[0] - 1][valor[1] - 1] = X


# desenha o tabuleiro
def desenhaTabuleiro(colunas=5):
    print("\n   _|  ", end="")
    for i in range(1, colunas + 1):
        print(f"\033[1;35m{i}\033[m" + "  ", end="")

    print("|")
    for i, j in enumerate(jogo):
        print(f" \033[1;35m{i+1}\033[m", " |" + "  " + "  ".join(j) + "  |")
    print()


instrucoes()

while True:
    # jogo = [[X, X, X, X, X],
    #         [X, X, X, X, X],
    #         [X, X, X, X, X],
    #         [X, X, X, X, X],
    #         [X, X, X, X, X]]

    jogo = [
        [O, X, O, O, O],
        [X, X, X, O, O],
        [O, X, O, X, O],
        [O, O, X, X, X],
        [O, O, O, X, O],
    ]

    jogadas = jogadasRestantes = menuGame()

    if jogadas > 0:

        while validacao():

            desenhaTabuleiro()

            if jogadasRestantes > 0:  # Verifica se ainda existem jogadas
                line, col = validaEntrada()
                xpto = verificaBorda(line, col)

                aplicaJogada(xpto)

                jogadasRestantes -= 1
                print(f"Número de jogadas restantes : {jogadasRestantes}")

            else:
                # Fim do jogo
                print("Acabou o seu número de jogadas!")
                print("\033[1m -- Fim de Game! -- \033[m")
                break

        if not validacao():

            desenhaTabuleiro()
            
            print("\n", "  \U0001F388\U0001F388\U0001F388"*5, end="\n\n")
            print(
                f"  \U0001F38A \U0001F38A  \033[1mParabéns!  \U0001F973 \U0001F973  Você ganhou o Jogo das Luzes em {jogadas-jogadasRestantes} jogadas  \U0001F389 \U0001F389 \033[m")
            print("\n", "  \U0001F388\U0001F388\U0001F388"*5, end="\n\n")

            nome = input("Digite o seu nome: ")
            # Abre o arquivo txt e coloca o nome e o número de tentativas em um vetor
            linhas = openFile()
            
            mem = [ [int(j.split(",")[1].rstrip()), j.split(",")[0]] for j in linhas] if len(linhas) > 0 else []
            # with open('ranking_jogo.txt', mode='r', encoding='utf-8') as f:
            #     for jogadores in enumerate(f):
            #         mem.append([
            #             int(jogadores.split(' ')[2]),
            #             jogadores.split(' ')[0]
            #         ])

            mem.append([jogadas - jogadasRestantes, nome])
            mem = sorted(mem)
            print(mem)

            # with open('ranking_jogo.txt', mode='w', encoding='utf-8') as f:
            #     for i in mem:
            #         f.write(f'{i[1]}, {i[0]} tentativas\n')

    elif jogadas == 0:
        print("\nSaindo do jogo . . .")
        break
