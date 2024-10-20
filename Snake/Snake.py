import pygame
import random

#Inicia o Pygame
pygame.init()
#Define o nome do jogo
pygame.display.set_caption("Snake")
#Define a altura e largura da tela
largura,altura = 1000,600
Tela = pygame.display.set_mode((largura,altura))

#Cria o relógio interno do jogo
Relogio = pygame.time.Clock()

#Define as variáveis para cada uma das cores utilizadas ao longo do código
Preto = (0,0,0)
Branco = (255,255,255)
Vermelho = (255,0,0)
Verde = (0,255,0)
Azul = (0,0,255)

#Define os parametros do jogo
TamanhoCubos = 20
FatorVelocidade = 10

#Controla o local de surgimento das maçãs
def GerarMaca():
    MacaX = round(random.randrange(0,largura - TamanhoCubos)/20.0)*20.0
    MacaY = round(random.randrange(0,altura - TamanhoCubos)/20.0)*20.0
    return MacaX,MacaY

#Desenha a maçã na tela
def DesenharMaca(TamanhoCubos,MacaX,MacaY):
    pygame.draw.rect(Tela,Verde,[MacaX,MacaY,TamanhoCubos,TamanhoCubos])

def DesenharCobrinha(TamanhoCubos, PixelsCobra):
    for Pixel in PixelsCobra:
        pygame.draw.rect(Tela,Branco,[Pixel[0],Pixel[1],TamanhoCubos,TamanhoCubos])

def DesenharPlacar(Pontuacao):
    Fonte = pygame.font.SysFont("Helveica", 40)
    Texto = Fonte.render(f"Pontuação: {Pontuacao}", True, Azul)
    Tela.blit(Texto, [1,1])

def MudarVelociade(Tecla):
    if Tecla == pygame.K_DOWN or Tecla == pygame.K_s:
        VelocidadeX = 0
        VelocidadeY = TamanhoCubos
    elif Tecla == pygame.K_UP or Tecla == pygame.K_w:
        VelocidadeX = 0
        VelocidadeY = -TamanhoCubos
    elif Tecla == pygame.K_RIGHT or Tecla == pygame.K_d:
        VelocidadeX = TamanhoCubos
        VelocidadeY = 0
    elif Tecla == pygame.K_LEFT or Tecla == pygame.K_a:
        VelocidadeX = -TamanhoCubos
        VelocidadeY = 0

    return VelocidadeX, VelocidadeY

#Define, cria e executa o jogo
def Jogo():
    #Variavel de EngGame
    FimDoJogo = False

    #Variaveis para posição da cobrinha
    X = largura/2
    Y = altura/2
    #Variaveis para controlar a velocidade e sentido da cobrinha
    VelocidadeX = 0
    VelocidadeY = 0
    #Variavel e lista para controlar o tamanho da cobrinha
    TamanhoCobrinha = 1
    PixelsCobra = []

    #Variaveis para controlar o local da maçã
    MacaX,MacaY = GerarMaca()

    #Coleta as ações feitas pelo jogador
    while not FimDoJogo:
        #Modifica a tela criada anteriormente
        Tela.fill(Preto)

        for Acao in pygame.event.get():
            if Acao.type == pygame.QUIT:
                FimDoJogo = True
            elif Acao.type == pygame.KEYDOWN:
                VelocidadeX, VelocidadeY = MudarVelociade(Acao.key)
        
        #Desenha a maca na tela
        DesenharMaca(TamanhoCubos,MacaX,MacaY)

        #Confere se a cobrinha colidiu com a parede
        if X<0 or X >= largura or Y<0 or Y>=altura:
            FimDoJogo = True

        #Atualizar a posição da cobrinha na tela
        X += VelocidadeX
        Y += VelocidadeY
        
        #Move a cobrinha na tela
        PixelsCobra.append([X, Y])
        if len(PixelsCobra) > TamanhoCobrinha:
            del PixelsCobra[0]
        #Checa as colisões da cobrinha com ela mesma
        for Pixel in PixelsCobra[:-1]:
            if Pixel == [X, Y]:
                FimDoJogo = True

        #Desenha a cobrinha na tela
        DesenharCobrinha(TamanhoCubos, PixelsCobra)

        #Desenha o placar do jogo
        DesenharPlacar(TamanhoCobrinha - 1)

        #Atualiza a tela
        pygame.display.update()

        #Caso a cobrinha coma a maçã
        if X == MacaX and Y == MacaY:
            TamanhoCobrinha += 1
            MacaX, MacaY = GerarMaca()

        #Define um timer entre cada update
        Relogio.tick(FatorVelocidade)

Jogo()