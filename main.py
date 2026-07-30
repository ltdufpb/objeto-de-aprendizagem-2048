import pygame
import random
import sys

# ########################################################################################################
# UNIDADE I - VARIÁVEIS, TIPOS DE DADOS E EXPRESSÕES
# ########################################################################################################

LARGURA_JANELA = 500
ALTURA_JANELA = 600


TAMANHO_GRADE = 4
TAMANHO_CELULA = 100
BORDA_CELULA = 10
MARGEM_TOPO = 80


COR_DE_FUNDO = (187, 173, 160)
COR_DO_TEXTO = (119, 110, 101)
TEXTO_CLARO = (249, 246, 242)
COR_LEGENDA = (150, 150, 150)


NOME_DO_JOGO = "2048 - Edição Pygame"



# ########################################################################################################
# UNIDADE II - ESTRUTURAS DE CONTROLE E ESTRUTURAS DE DADOS
# ########################################################################################################

CORES_CELULAS = {
    0: (205, 192, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

def comprimir(linha):
    nova_linha = [x for x in linha if x != 0]

    while len(nova_linha) < TAMANHO_GRADE:
        nova_linha.append(0)
    return nova_linha


def mesclar(linha):
    nova_linha = comprimir(linha) 

    for i in range(TAMANHO_GRADE - 1): 
        if nova_linha[i] == nova_linha[i + 1] and nova_linha[i] != 0:
            nova_linha[i] *= 2
            nova_linha[i + 1] = 0

    nova_linha = comprimir(nova_linha)
    return nova_linha


def mover_esquerda(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for i in range(TAMANHO_GRADE):
        linha_original = tabuleiro[i]

        tabuleiro[i] = mesclar(tabuleiro[i])

        if tabuleiro[i] != linha_original:
            estado_de_jogo["moveu"] = True


def mover_direita(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for i in range(TAMANHO_GRADE):
        linha_original = tabuleiro[i]

        tabuleiro[i] = tabuleiro[i][::-1]

        tabuleiro[i] = mesclar(tabuleiro[i])

        tabuleiro[i] = tabuleiro[i][::-1]

        if tabuleiro[i] != linha_original:
            estado_de_jogo["moveu"] = True


def mover_cima(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for j in range(TAMANHO_GRADE):

        coluna_original = []
        for i in range(TAMANHO_GRADE):
            coluna_original.append(tabuleiro[i][j])

        coluna = coluna_original

        coluna = mesclar(coluna)

        for i in range(TAMANHO_GRADE):
            tabuleiro[i][j] = coluna[i]

        if coluna != coluna_original:
            estado_de_jogo["moveu"] = True


def mover_baixo(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for j in range(TAMANHO_GRADE):

        coluna_original = []
        for i in range(TAMANHO_GRADE):
            coluna_original.append(tabuleiro[i][j])

        coluna = coluna_original

        coluna = coluna[::-1]
        coluna = mesclar(coluna)
        coluna = coluna[::-1]

        for i in range(TAMANHO_GRADE):
            tabuleiro[i][j] = coluna[i]
        if coluna != coluna_original:
            estado_de_jogo["moveu"] = True


def mover(direction, estado_de_jogo):
    if direction == "esquerda":
        mover_esquerda(estado_de_jogo)
    elif direction == "direita":
        mover_direita(estado_de_jogo)
    elif direction == "cima":
        mover_cima(estado_de_jogo)
    elif direction == "baixo":
        mover_baixo(estado_de_jogo)

    if estado_de_jogo["moveu"]:
        adicionar_celula(estado_de_jogo["tabuleiro"])


def iniciar_jogo():
    tabuleiro = [[0] * TAMANHO_GRADE for _ in range(TAMANHO_GRADE)]

    adicionar_celula(tabuleiro)
    adicionar_celula(tabuleiro)

    return {
        "tabuleiro": tabuleiro,
        "moveu": False,
    }


# ########################################################################################################
# UNIDADE III - Funções, Módulos e Bibliotecas
# ########################################################################################################


def adicionar_celula(tabuleiro):
    celulas_vazias = []

    for i in range(TAMANHO_GRADE):
        for j in range(TAMANHO_GRADE):
            if tabuleiro[i][j] == 0:
                celulas_vazias.append((i, j))


    if celulas_vazias:
        i, j = random.choice(celulas_vazias)

        tabuleiro[i][j] = random.choice([2, 2, 2, 2, 4])


pygame.init()

FONTE_GRANDE = pygame.font.Font(None, 55)
FONTE_MEDIA = pygame.font.Font(None, 40)
FONTE_PEQUENA = pygame.font.Font(None, 30)

janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))


def desenhar_jogo(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    janela.fill((250, 248, 246))

    titulo = [
        FONTE_GRANDE.render(NOME_DO_JOGO[0:7], True, COR_DO_TEXTO),
        FONTE_PEQUENA.render(NOME_DO_JOGO[7:], True, COR_DO_TEXTO),
    ]
    janela.blit(titulo[0], (20, 20))
    janela.blit(titulo[1], (140, 30))

    tabuleiro_top = MARGEM_TOPO
    tabuleiro_left = (
        LARGURA_JANELA
        - (TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA)
    ) // 2

    pygame.draw.rect(
        janela,
        COR_DE_FUNDO,
        (
            tabuleiro_left - 5,
            tabuleiro_top - 5,
            TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA + 10,
            TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA + 10,
        ),
    )


    for i in range(TAMANHO_GRADE):
        for j in range(TAMANHO_GRADE):
            x = tabuleiro_left + j * (TAMANHO_CELULA + BORDA_CELULA)
            y = tabuleiro_top + i * (TAMANHO_CELULA + BORDA_CELULA)

            valor = tabuleiro[i][j]

            color = CORES_CELULAS.get(valor, CORES_CELULAS[2048])

            pygame.draw.rect(janela, color, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))

            if valor != 0:
                if valor <= 8:
                    texto = FONTE_GRANDE.render(str(valor), True, COR_DO_TEXTO)
                elif valor < 1024:
                    texto = FONTE_MEDIA.render(str(valor), True, COR_DO_TEXTO)
                else:
                    texto = FONTE_PEQUENA.render(str(valor), True, TEXTO_CLARO)

                texto_rect = texto.get_rect(
                    center=(x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2)
                )
                janela.blit(texto, texto_rect)


    legenda = [
        FONTE_PEQUENA.render("Use WASD ou as setas para movimentar", True, COR_LEGENDA),
        FONTE_PEQUENA.render("R para reiniciar", True, COR_LEGENDA),
        FONTE_PEQUENA.render("Q para fechar", True, COR_LEGENDA),
    ]

    janela.blit(legenda[0], (tabuleiro_left, ALTURA_JANELA - 75))
    janela.blit(legenda[1], (tabuleiro_left, ALTURA_JANELA - 50))
    janela.blit(legenda[2], (tabuleiro_left, ALTURA_JANELA - 25))


    pygame.display.flip()


def main():
    estado_de_jogo = iniciar_jogo()
    pygame.display.set_caption(NOME_DO_JOGO)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    mover("esquerda", estado_de_jogo)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    mover("direita", estado_de_jogo)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    mover("cima", estado_de_jogo)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    mover("baixo", estado_de_jogo)

                elif event.key == pygame.K_r:
                    estado_de_jogo = iniciar_jogo()

                elif event.key == pygame.K_q:
                    running = False

        desenhar_jogo(estado_de_jogo)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
