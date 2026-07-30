import pygame  # U3 - Estudo de caso (PyGame): importando biblioteca externa de jogos
import random  # U3 - Biblioteca padrão: importando módulo de aleatoriedade
import sys     # U3 - Biblioteca padrão: importando módulo do sistema operacional

# ########################################################################################################
# UNIDADE I - VARIÁVEIS, TIPOS DE DADOS E EXPRESSÕES
# ########################################################################################################


#--------------------------------------------------------------------
# Configurações de tamanho da janela (Tipos Numéricos: Inteiros)
#------------------------------------------------------------------
LARGURA_JANELA = 500                                                # U1 - Variáveis e atribuições: definindo a largura da tela
ALTURA_JANELA = 600                                                 # U1 - Variáveis e atribuições: definindo a altura da tela

#-----------------------------------------------------------------------------------
# Configurações da grade do tabuleiro (Expressões Aritméticas e Variáveis)
#---------------------------------------------------------------------------------
TAMANHO_GRADE = 4                                                   # U1 - Variáveis e atribuições: quantidade de linhas e colunas
TAMANHO_CELULA = 100                                                # U1 - Variáveis e atribuições: tamanho em pixels de cada quadrado
BORDA_CELULA = 10                                                   # U1 - Variáveis e atribuições: espaçamento entre os quadrados
MARGEM_TOPO = 80                                                    # U1 - Variáveis e atribuições: espaço para o título no topo

#-----------------------------------------------------------------------------------------------------
# Definição de Cores no formato RGB (Modifique os números de 0 a 255)
# OBS: O formato (R, G, B) é uma Tupla (Unidade II), mas tratada aqui como valor de atribuição.
#---------------------------------------------------------------------------------------------------
COR_DE_FUNDO = (187, 173, 160)                                      # U1 - Variáveis e atribuições: cor de fundo do tabuleiro
COR_DO_TEXTO = (119, 110, 101)                                      # U1 - Variáveis e atribuições: cor dos números baixos e título
TEXTO_CLARO = (249, 246, 242)                                       # U1 - Variáveis e atribuições: cor dos números altos

#-----------------------------------------------
# Texto do Título (Tipo de Dado: String)
#---------------------------------------------
NOME_DO_JOGO = "2048 - Edição Pygame"                               # U1 - Tipos de dados: strings; U1 - Variáveis e atribuições


""" 
# ################################################################################
# BLOCO DE ENTRADA VIA TERMINAL (OPCIONAL E REMOVÍVEL)
# Esta seção é autocontida. Você pode apagar sem afetar o funcionamento do jogo:
# Remova as aspas triplas acima e abaixo deste bloco para utilizar a entrada de nome do jogador via terminal.
# o NOME_DO_JOGO definido acima continuará valendo.
# ##############################################################################

print("==================================================")         # U1 - Entrada e saída: exibindo mensagem de boas-vindas no terminal
print("INSERINDO NOME DO JOGADOR VIA CONSOLE")                      # U1 - Entrada e saída: exibindo interface textual
print("==================================================")         # U1 - Entrada e saída: exibindo linha divisória

NOME_JOGADOR = input("Digite o nome do jogador: ")                  # U1 - Entrada e saída: recebendo texto do usuário
if len(NOME_JOGADOR) > 21:                                          # U1 - Estruturas de controle: if: limitando o tamanho do nome
    NOME_DO_JOGO = "2048 - Jogador de nome longo"                   # U1 - Variáveis e atribuições
else:                                                               # U1 - Estruturas de controle: else
    NOME_DO_JOGO = "2048 - Jogador: " + NOME_JOGADOR                # U1 - Tipos de dados: strings: concatenação

"""

# ########################################################################################################
# UNIDADE II - ESTRUTURAS DE CONTROLE E ESTRUTURAS DE DADOS
# ########################################################################################################


#--------------------------------------------------------------------------------------------------------------------------------
# Dicionário que mapeia os valores das peças para suas cores correspondentes, com um valor padrão para peças maiores que 2048
#------------------------------------------------------------------------------------------------------------------------------
CORES_CELULAS = {                 # U2 - Estruturas de dados: dicionários: mapeando valores para cores
    0: (205, 192, 180),           # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    2: (238, 228, 218),           # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    4: (237, 224, 200),           # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    8: (242, 177, 121),           # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    16: (245, 149, 99),           # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    32: (246, 124, 95),           # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    64: (246, 94, 59),            # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    128: (237, 207, 114),         # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    256: (237, 204, 97),          # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    512: (237, 200, 80),          # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    1024: (237, 197, 63),         # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
    2048: (237, 194, 46),         # U2 - Dicionários: par chave(int)-valor(tupla); U2 - Tuplas
}


#---------------------------------------------------------------------------------------------
# COMPRIMIR: empurra os números de uma linha para a esquerda, removendo os zeros do meio
# Exemplo: [2, 0, 0, 2]  ->  [2, 2, 0, 0]
#------------------------------------------------------------------------------------------
def comprimir(linha):                                                       # U3 - Funções: definição com parâmetro e retorno
    
    #----------------------------------------------------------
    # Remove zeros, colocando os números no inicio da linha
    #------------------------------------------------------
    nova_linha = [x for x in linha if x != 0]                               # U2 - Estruturas de dados: listas: Compreensão
    
    #-----------------------------------
    # preenchendo o restante com zeros
    #-----------------------------------
    while len(nova_linha) < TAMANHO_GRADE:                                  # U2 - Estruturas de controle: while: repetindo enquanto faltar espaço
        nova_linha.append(0)                                                # U2 - Estruturas de dados: listas: preenchendo com zero
    return nova_linha                                                       # U3 - Funções: retorno de valor



#------------------------------------------------------------------------------------------------------------------------
# Função que mescla as células de uma linha, somando os números iguais adjacentes e atualizando a pontuação
#----------------------------------------------------------------------------------------------------------------
def mesclar(linha):                                                         # U3 - Funções: definição com parâmetro
    nova_linha = comprimir(linha)                                           # U3 - Funções: chamada de função (composição de funções)

    #-----------------------------------------------------------------------------------------
    # Percorre a linha e verifica se há números iguais adjacentes (diferentes de zero),
    # se houver, soma os números e zera o número adjacente
    #------------------------------------------------------------------------------------
    for i in range(TAMANHO_GRADE - 1):                                      # U2 - Estruturas de controle: for com range
        if nova_linha[i] == nova_linha[i + 1] and nova_linha[i] != 0:       # U1 - Estruturas de controle: if com operadores lógicos (and) e relacionais
            nova_linha[i] *= 2                                              # U1 - Variáveis e atribuições / Expressões: atribuição composta (*=)
            nova_linha[i + 1] = 0                                           # U1 - Variáveis e atribuições: zerando elemento mesclado
    
    nova_linha = comprimir(nova_linha)                                      # U3 - Funções: chamada de função novamente para reorganizar lista
    return nova_linha                                                       # U3 - Funções: retorno de valor



#-----------------------------------------------------
# Função para mover os números para a esquerda,
# comprime e mescla cada linha do tabuleiro,
# e atualizando o status de movimento
#------------------------------------------------
def mover_esquerda(estado_de_jogo):                                         # U3 - Funções: definição com parâmetro (dicionário)
    tabuleiro = estado_de_jogo["tabuleiro"]                                 # U2 - Dicionários: acesso a valor por chave; U1 - Variáveis e atribuições
    estado_de_jogo["moveu"] = False                                         # U2 - Dicionários: atribuição de valor; U1 - Tipos de dados: booleanos
    for i in range(TAMANHO_GRADE):                                          # U2 - Estruturas de controle: for
        linha_original = tabuleiro[i]                                       # U1 - Variáveis e atribuições: guardando referência da linha original

        tabuleiro[i] = mesclar(tabuleiro[i])                                # U3 - Funções: chamada de função; U1 - Atribuições: atualizando linha

        #------------------------------------------------------------------------------------
        # Se a linha resultante for diferente da linha original, 
        # isso indica que houve um movimento (números foram movidos ou mesclados),
        #----------------------------------------------------------------------------
        if tabuleiro[i] != linha_original:                                  # U1 - Estruturas de controle: if com operador relacional (!=)
            estado_de_jogo["moveu"] = True                                  # U2 - Dicionários: atualizando valor; U1 - Tipos de dados: booleanos



#-----------------------------------------------------------------
# Mesma coisa para a direita, mas
# invertendo a linha antes de comprimir e mesclar,
# e invertendo novamente depois
#------------------------------------------------------------
def mover_direita(estado_de_jogo):                                          # U3 - Funções: definição com parâmetro
    tabuleiro = estado_de_jogo["tabuleiro"]                                 # U2 - Dicionários: acesso a valor por chave
    estado_de_jogo["moveu"] = False                                         # U2 - Dicionários: atribuição; U1 - Tipos de dados: booleanos
    for i in range(TAMANHO_GRADE):                                          # U2 - Estruturas de controle: for
        linha_original = tabuleiro[i]                                       # U1 - Variáveis e atribuições

        #------------------------------------------------------------------------------------------------------------------------
        # Inverte a linha para tratar o movimento para a direita como se fosse para a esquerda
        # A notação [::-1] separa uma "fatia" do array seguindo a lógica de [início:fim:passo]
        # Ou seja, o passo -1 indica que o array deve ser percorrido de trás para frente, invertendo a ordem dos elementos
        #-------------------------------------------------------------------------------------------------------------------
        tabuleiro[i] = tabuleiro[i][::-1]                                   # U2 - Estruturas de dados: listas: fatiamento (slicing) com passo -1

        tabuleiro[i] = mesclar(tabuleiro[i])                                # U3 - Funções: chamada de função

        tabuleiro[i] = tabuleiro[i][::-1]                                   # U2 - Estruturas de dados: listas: fatiamento para restaurar ordem

        if tabuleiro[i] != linha_original:                                  # U1 - Estruturas de controle: if com operador relacional (!=)
            estado_de_jogo["moveu"] = True                                  # U2 - Dicionários: atribuição; U1 - Tipos de dados: booleanos




#------------------------------------------------------------------------------------------------
# Para mover para cima ou para baixo, precisamos trabalhar com as colunas do tabuleiro,
# extraindo as colunas, comprimindo e mesclando como se fossem linhas
#---------------------------------------------------------------------------------------
def mover_cima(estado_de_jogo):                                             # U3 - Funções: definição com parâmetro
    tabuleiro = estado_de_jogo["tabuleiro"]                                 # U2 - Dicionários: acesso a valor por chave
    estado_de_jogo["moveu"] = False                                         # U2 - Dicionários: atribuição; U1 - Tipos de dados: booleanos
    for j in range(TAMANHO_GRADE):                                          # U2 - Estruturas de controle: for: percorrendo colunas

        #--------------------------------------
        # Extraindo a coluna j do tabuleiro
        #------------------------------------
        coluna_original = []                                                # U1 - Tipos de dados: listas: criando lista vazia
        for i in range(TAMANHO_GRADE):                                      # U2 - Estruturas de controle: for aninhado: percorrendo linhas
            coluna_original.append(tabuleiro[i][j])                         # U1 - Tipos de dados: listas: montando coluna a partir do tabuleiro

        #--------------------------------------------------------------
        # Guardando estado original da coluna para verificar se houve movimento
        #------------------------------------------------------------
        coluna = coluna_original                                            # U1 - Variáveis e atribuições

        coluna = mesclar(coluna)                                            # U3 - Funções: chamada de função
        
        #------------------------------------------------------------------------------------------------------------
        # Aqui utilizamos um for normal ao invés de list comprehension para atualizar a coluna do tabuleiro
        # pois precisamos do valor de i tanto em tabuleiro[i][j] quanto em coluna[i]
        #------------------------------------------------------------------------------------------------
        for i in range(TAMANHO_GRADE):                                      # U2 - Estruturas de controle: for: atualizando coluna no tabuleiro
            tabuleiro[i][j] = coluna[i]                                     # U1 - Variáveis e atribuições: escrevendo valor de volta na matriz

        if coluna != coluna_original:                                       # U1 - Estruturas de controle: if com operador relacional (!=)
            estado_de_jogo["moveu"] = True                                  # U2 - Dicionários: atribuição; U1 - Tipos de dados: booleanos



def mover_baixo(estado_de_jogo):                                            # U3 - Funções: definição com parâmetro
    tabuleiro = estado_de_jogo["tabuleiro"]                                 # U2 - Dicionários: acesso a valor por chave
    estado_de_jogo["moveu"] = False                                         # U2 - Dicionários: atribuição; U1 - Tipos de dados: booleanos
    for j in range(TAMANHO_GRADE):                                          # U2 - Estruturas de controle: for: percorrendo colunas

        coluna_original = []                                                # U1 - Tipos de dados: listas: criando lista vazia
        for i in range(TAMANHO_GRADE):                                      # U2 - Estruturas de controle: for aninhado
            coluna_original.append(tabuleiro[i][j])                         # U1 - Tipos de dados: listas: montando coluna

        coluna = coluna_original                                            # U1 - Variáveis e atribuições

        coluna = coluna[::-1]                                               # U2 - Estruturas de dados: listas: fatiamento com passo -1
        coluna = mesclar(coluna)                                            # U3 - Funções: chamada de função
        coluna = coluna[::-1]                                               # U2 - Estruturas de dados: listas: fatiamento para restaurar ordem

        for i in range(TAMANHO_GRADE):                                      # U2 - Estruturas de controle: for: escrevendo coluna de volta
            tabuleiro[i][j] = coluna[i]                                     # U1 - Variáveis e atribuições
        if coluna != coluna_original:                                       # U1 - Estruturas de controle: if com operador relacional (!=)
            estado_de_jogo["moveu"] = True                                  # U2 - Dicionários: atribuição; U1 - Tipos de dados: booleanos





#------------------------------------------------------------------------------------------------
# Função para mover os números em uma direção específica (esquerda, direita, cima ou baixo),
# chamando a função de movimento correspondente
#-------------------------------------------------------------------------------------------
def mover(direction, estado_de_jogo):                                       # U3 - Funções: definição com múltiplos parâmetros
    if direction == "left":                                                 # U1 - Estruturas de controle: if-elif-else: verificando direção
        mover_esquerda(estado_de_jogo)                                      # U3 - Funções: chamada de função
    elif direction == "right":                                              # U1 - Estruturas de controle: elif
        mover_direita(estado_de_jogo)                                       # U3 - Funções: chamada de função
    elif direction == "up":                                                 # U1 - Estruturas de controle: elif
        mover_cima(estado_de_jogo)                                          # U3 - Funções: chamada de função
    elif direction == "down":                                               # U1 - Estruturas de controle: elif
        mover_baixo(estado_de_jogo)                                         # U3 - Funções: chamada de função

    #---------------------------------------------------
    # Se houve um movimento, adiciona uma nova peça
    #------------------------------------------------
    if estado_de_jogo["moveu"]:                                             # U1 - Estruturas de controle: if; U2 - Dicionários: acesso por chave; U1 - Booleanos
        adicionar_celula(estado_de_jogo["tabuleiro"])                       # U3 - Funções: chamada de função; U2 - Dicionários: acesso por chave



#------------------------------------------------------------------------------------------------------------
# Função para inicializar o estado do jogo, criando o tabuleiro e adicionando as peças iniciais
#------------------------------------------------------------------------------------------------
def iniciar_jogo():                                                         # U3 - Funções: definição de função sem parâmetros

    #------------------------------------------------------------------------------------------------
    # O conteúdo do tabuleiro é representado por uma matriz 4x4,
    # onde cada célula pode conter um número (2, 4, 8, etc.) ou 0 para indicar que está vazia.
    #------------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------
    # Cria uma linha com 4 células vazias (valor 0) e adiciona ao tabuleiro
    #------------------------------------------------------------------------
    tabuleiro = [[0] * TAMANHO_GRADE for _ in range(TAMANHO_GRADE)]         # U2 - Estruturas de dados: listas: Compreensão

    #------------------------------------------------------------------
    # Adiciona duas peças iniciais no tabuleiro, chamando a função
    #---------------------------------------------------------------
    adicionar_celula(tabuleiro)                                             # U3 - Funções: chamada de função com argumento
    adicionar_celula(tabuleiro)                                             # U3 - Funções: chamada de função com argumento

    #---------------------------------------------------------------------
    # Retorna um dicionário com o estado do jogo, incluindo o tabuleiro
    # e o status de movimento (moveu)
    #------------------------------------------------------------------
    return {                                                                # U3 - Funções: retorno de valor; U2 - Estruturas de dados: dicionários
        "tabuleiro": tabuleiro,                                             # U2 - Dicionários: par chave(string)-valor(lista); U1 - Tipos de dados: strings
        "moveu": False,                                                     # U2 - Dicionários: par chave(string)-valor(booleano); U1 - Tipos de dados: booleanos
    }




# ########################################################################################################
# UNIDADE III - Funções, Módulos e Bibliotecas
# ########################################################################################################

#-------------------------------------------------------------------------------------
# Função para adicionar uma nova peça (2 ou 4) em uma célula vazia do tabuleiro
#--------------------------------------------------------------------------------
def adicionar_celula(tabuleiro):                                            # U3 - Funções: definição com parâmetro
    celulas_vazias = []                                                     # U1 - Tipos de dados: listas: criando lista vazia para posições livres

    #-----------------------------------------------------------------------------------------------
    # Percorre o tabuleiro para encontrar células vazias (com valor 0) e armazena suas posições
    #-------------------------------------------------------------------------------------------
    for i in range(TAMANHO_GRADE):                                          # U2 - Estruturas de controle: for: percorrendo linhas
        for j in range(TAMANHO_GRADE):                                      # U2 - Estruturas de controle: for: percorrendo colunas (for aninhado)
            if tabuleiro[i][j] == 0:                                        # U1 - Estruturas de controle: if: verificando célula vazia
                celulas_vazias.append((i, j))                               # U1 - Tipos de dados: listas / U2 - Tuplas: adicionando posição como tupla

    #--------------------------------------------------------------------------------------
    # Se houver células vazias, escolhe uma aleatoriamente e atribui a ela o valor 2 ou 4
    #--------------------------------------------------------------------------------------
    if celulas_vazias:                                                      # U1 - Estruturas de controle: if: verificando se a lista não está vazia
        i, j = random.choice(celulas_vazias)                                # U3 - Biblioteca padrão: escolha aleatória; U2 - Tuplas: desempacotamento

        #---------------------------------------------------------------------------------------------------------------------------------------
        # A função random.choice é usada para escolher aleatoriamente um item do array [2, 2, 2, 2, 4] para ser adicionado ao tabuleiro
        # 2 aparece quatro vezes no array para que a probabilidade de escolher 2 seja quatro vezes maior do que escolher 4
        #-------------------------------------------------------------------------------------------------------------------------------
        tabuleiro[i][j] = random.choice([2, 2, 2, 2, 4])                    # U3 - Biblioteca padrão: random.choice; U1 - Listas e atribuição



#----------------------------------------
# Inicializando módulos do Pygame
#-----------------------------------
pygame.init()                                                               # U3 - Estudo de caso (PyGame): inicializando todos os módulos do pygame

#-------------------------------------------------------------------------------------------------------------------
# Tamanhos das fontes dos números. Números maiores precisam ter uma fonte menor para caberem dentro da célula
#--------------------------------------------------------------------------------------------------------------
FONTE_GRANDE = pygame.font.Font(None, 55)                                   # U3 - Estudo de caso (PyGame): criando objeto de fonte
FONTE_MEDIA = pygame.font.Font(None, 40)                                    # U3 - Estudo de caso (PyGame): criando objeto de fonte
FONTE_PEQUENA = pygame.font.Font(None, 30)                                  # U3 - Estudo de caso (PyGame): criando objeto de fonte

#--------------------------------------------------------------------------------
# Criando a janela do jogo e o relógio para controlar a taxa de atualização
#---------------------------------------------------------------------------
janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))           # U3 - Estudo de caso (PyGame): criando janela gráfica



#--------------------------------------------------
# Função para desenhar o estado do jogo na tela,
# incluindo o tabuleiro e as peças
#---------------------------------------------
def desenhar_jogo(estado_de_jogo):                                          # U3 - Funções: definição com parâmetro
    tabuleiro = estado_de_jogo["tabuleiro"]                                 # U2 - Dicionários: acesso a valor por chave
    janela.fill((250, 248, 246))                                            # U3 - Estudo de caso (PyGame): preenchendo fundo da janela com cor RGB

    #--------------------
    # Título do jogo
    #-----------------
    titulo = [
        FONTE_GRANDE.render(NOME_DO_JOGO[0:7], True, COR_DO_TEXTO),         # U3 - Estudo de caso (PyGame): renderizando texto; U1 - Strings
        FONTE_PEQUENA.render(NOME_DO_JOGO[7:], True, COR_DO_TEXTO)          # U3 - Estudo de caso (PyGame): desenhando superfície na janela
        ]  
    janela.blit(titulo[0], (20, 20))
    janela.blit(titulo[1], (140, 30))                                

    #-----------------------------------------------------------------
    # Calcula a posição do tabuleiro para centralizá-lo na tela
    #------------------------------------------------------------
    tabuleiro_top = MARGEM_TOPO                                                                                     # U1 - Variáveis e atribuições
    tabuleiro_left = (LARGURA_JANELA - (TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA)) // 2  # U1 - Expressões aritméticas: calculando margem horizontal

    #------------------------------------------------------------------------------------------
    # Desenha o fundo do tabuleiro, criando um retângulo maior para dar um efeito de borda
    #-------------------------------------------------------------------------------------
    pygame.draw.rect(
        janela,                                                                         # U3 - Estudo de caso (PyGame): referência à superfície da janela
        COR_DE_FUNDO,                                                                   # U3 - Estudo de caso (PyGame): cor do retângulo; U1 - Variáveis
        (
            tabuleiro_left - 5,                                                         # U1 - Expressões aritméticas: calculando posição x
            tabuleiro_top - 5,                                                          # U1 - Expressões aritméticas: calculando posição y
            TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA + 10,   # U1 - Expressões aritméticas: calculando largura
            TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA + 10,   # U1 - Expressões aritméticas: calculando altura
        ),
    )

    #---------------------------------------------------------------------------
    # Desenha as peças do tabuleiro, iterando sobre cada célula
    # desenhando um retângulo com a cor correspondente ao valor da peça,
    # e desenhando o número da peça centralizado dentro do retângulo
    #----------------------------------------------------------------------
    for i in range(TAMANHO_GRADE):                                                      # U2 - Estruturas de controle: for: iterando sobre linhas
        for j in range(TAMANHO_GRADE):                                                  # U2 - Estruturas de controle: for aninhado: iterando sobre colunas
            x = tabuleiro_left + j * (TAMANHO_CELULA + BORDA_CELULA)                    # U1 - Variáveis e atribuições / Expressões aritméticas: posição x da célula
            y = tabuleiro_top + i * (TAMANHO_CELULA + BORDA_CELULA)                     # U1 - Variáveis e atribuições / Expressões aritméticas: posição y da célula

            valor = tabuleiro[i][j]                                                     # U1 - Variáveis e atribuições: lendo valor da célula na matriz do tabuleiro

            #------------------------------------------------------------
            # Obtém a cor correspondente ao valor da peça,
            # usando o dicionário CORES_CELULAS 
            # (com um valor padrão para peças maiores que 2048)
            #-------------------------------------------------------
            color = CORES_CELULAS.get(valor, CORES_CELULAS[2048])                       # U2 - Dicionários: método .get() com valor padrão
            
            #------------------------------------------------------------
            # Desenha o retângulo da peça com a cor correspondente
            #-------------------------------------------------------
            pygame.draw.rect(janela, color, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))     # U3 - Estudo de caso (PyGame): desenhando retângulo
            
            #-----------------------------------------------------------------
            # Se a peça não for vazia (valor diferente de 0), 
            # desenha o número da peça centralizado dentro do retângulo
            #------------------------------------------------------------
            if valor != 0:                                                              # U1 - Estruturas de controle: if: verificando célula não vazia
                if valor <= 4:                                                          # U1 - Estruturas de controle: if-elif-else: escolhendo tamanho da fonte
                    texto = FONTE_GRANDE.render(str(valor), True, COR_DO_TEXTO)         # U3 - Estudo de caso (PyGame): renderizando número como texto
                elif valor < 1024:                                                      # U1 - Estruturas de controle: elif
                    texto = FONTE_MEDIA.render(str(valor), True, COR_DO_TEXTO)          # U3 - Estudo de caso (PyGame): renderizando com fonte média
                else:                                                                   # U1 - Estruturas de controle: else
                    texto = FONTE_PEQUENA.render(str(valor), True, TEXTO_CLARO)         # U3 - Estudo de caso (PyGame): renderizando com fonte pequena

                texto_rect = texto.get_rect(
                    center=(x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2)           # U3 - Estudo de caso (PyGame): centralizando texto na célula; U1 - Expressões
                )
                janela.blit(texto, texto_rect)                                          # U3 - Estudo de caso (PyGame): desenhando texto na tela

    #--------------------------------------------------
    # Exibe instruções na parte inferior da tela
    #---------------------------------------------
    legenda = [                                                                         # U1 - Tipos de dados: listas: lista de superfícies de texto
        FONTE_PEQUENA.render(
            "Use WASD ou as setas para movimentar", True, (150, 150, 150)               # U3 - Estudo de caso (PyGame): renderizando instrução; U1 - Strings
        ),
        FONTE_PEQUENA.render("R para reiniciar", True, (150, 150, 150)),
        FONTE_PEQUENA.render("Q para fechar", True, (150, 150, 150)),                   # U3 - Estudo de caso (PyGame): renderizando instrução; U1 - Strings
    ]

    #---------------------------------------------
    # Funções que escrevem as instruções na tela
    #----------------------------------------
    janela.blit(legenda[0], (tabuleiro_left, ALTURA_JANELA - 75))                       # U3 - Estudo de caso (PyGame): desenhando legenda; U1 - Listas: acesso por índice
    janela.blit(legenda[1], (tabuleiro_left, ALTURA_JANELA - 50))                       # U3 - Estudo de caso (PyGame): desenhando legenda; U1 - Listas: acesso por índice
    janela.blit(legenda[2], (tabuleiro_left, ALTURA_JANELA - 25))                       # U3 - Estudo de caso (PyGame): desenhando legenda; U1 - Listas: acesso por índice

    #-------------------------------------------------------
    # Atualiza a tela para mostrar as mudanças feitas
    #--------------------------------------------------
    pygame.display.flip()                                                               # U3 - Estudo de caso (PyGame): atualizando a janela (renderizando frame)



def main():                                                                             # U3 - Funções: definição da função principal sem parâmetros
    estado_de_jogo = iniciar_jogo()                                                     # U3 - Funções: chamada de função com retorno; U1 - Variáveis e atribuições
    pygame.display.set_caption(NOME_DO_JOGO)                                            # U3 - Estudo de caso (PyGame): definindo título da janela; U1 - Strings

    running = True                                                                      # U1 - Variáveis e atribuições; U1 - Tipos de dados: booleanos

    #--------------------------------------------------
    # Game loop principal, que continua rodando
    # enquanto a variável running for igual a True,
    #-----------------------------------------------
    while running:                                                                      # U2 - Estruturas de controle: while: loop principal do jogo
        for event in pygame.event.get():                                                # U2 - Estruturas de controle: for: percorrendo eventos do pygame; U3 - PyGame
            if event.type == pygame.QUIT:                                               # U1 - Estruturas de controle: if: verificando evento de fechar janela
                running = False                                                         # U1 - Variáveis e atribuições; U1 - Tipos de dados: booleanos

            #--------------------------------------------------
            # Verifica se uma tecla foi pressionada 
            # e chama a função de movimento correspondente
            #-----------------------------------------------
            if event.type == pygame.KEYDOWN:                                            # U1 - Estruturas de controle: if: verificando evento de tecla pressionada
                if event.key in [pygame.K_LEFT, pygame.K_a]:                            # U1 - Estruturas de controle: if; U1 - Listas; operador 'in'
                    mover("left", estado_de_jogo)                                       # U3 - Funções: chamada de função; U1 - Strings
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:                         # U1 - Estruturas de controle: elif
                    mover("right", estado_de_jogo)                                      # U3 - Funções: chamada de função; U1 - Strings
                elif event.key in [pygame.K_UP, pygame.K_w]:                            # U1 - Estruturas de controle: elif
                    mover("up", estado_de_jogo)                                         # U3 - Funções: chamada de função; U1 - Strings
                elif event.key in [pygame.K_DOWN, pygame.K_s]:                          # U1 - Estruturas de controle: elif
                    mover("down", estado_de_jogo)                                       # U3 - Funções: chamada de função; U1 - Strings

                #-------------------------------------------------------
                # Se a tecla R for pressionada, 
                # reinicia o jogo chamando a função iniciar_jogo
                #--------------------------------------------------
                elif event.key == pygame.K_r:                                           # U1 - Estruturas de controle: elif
                    estado_de_jogo = iniciar_jogo()                                     # U3 - Funções: chamada de função; U1 - Variáveis e atribuições

                #--------------------------------------------------
                # Se a tecla Q for pressionada, 
                # encerra o jogo definindo running como False
                #---------------------------------------------
                elif event.key == pygame.K_q:                                           # U1 - Estruturas de controle: elif
                    running = False                                                     # U1 - Variáveis e atribuições; U1 - Tipos de dados: booleanos

        #---------------------------------------------
        # Desenha o estado atual do jogo na tela 
        # e controla a taxa de atualização
        #----------------------------------------
        desenhar_jogo(estado_de_jogo)                                                   # U3 - Funções: chamada de função

    pygame.quit()                                                                       # U3 - Estudo de caso (PyGame): encerrando todos os módulos do pygame
    sys.exit()                                                                          # U3 - Biblioteca padrão: encerrando o processo Python




if __name__ == "__main__":                                                              # U3 - Biblioteca padrão: verificando se o script é executado diretamente
    main()                                                                              # U3 - Funções: chamada da função principal
