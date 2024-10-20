
import pygame
import random
import os

# Inicializa o pygame e seus módulos
pygame.init()
pygame.font.init()

# Define a altura e largura da tela
largura, altura = 500, 800

# Define o caminho base
base_path = os.path.dirname(__file__)  # Diretório atual do arquivo

# Cria o caminho para a pasta 'imgs'
imgs_path = os.path.join(base_path, 'imgs')

# Carrega as imagens utilizando o caminho criado anteriormente
ImagemFundo = pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, 'bg.png')))
ImagemCano = pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, 'pipe.png')))
ImagemChao = pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, 'base.png')))
ImagensPasssaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(imgs_path, 'bird3.png')))
]

# Define a fonte que será utilizada
FontePontuacao = pygame.font.SysFont("Arial", 36)

# Todas as informações e métodos do pássaro
class Passaro:
    Imgs = ImagensPasssaro
    RotacaoMaxima = 25
    VelocidadeDeRotacao = 20
    TempoAnimacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = y
        self.tempo = 0
        self.contagemDaImagem = 0
        self.imagem = self.Imgs[0]

    def Pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def MoverPassaro(self):
        self.tempo += 1
        Deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        if Deslocamento > 16:
            Deslocamento = 16
        elif Deslocamento < 0:
            Deslocamento -= 2

        self.y += Deslocamento

        if Deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.RotacaoMaxima:
                self.angulo = self.RotacaoMaxima
        else:
            if self.angulo > -90:
                self.angulo -= self.VelocidadeDeRotacao

    def DesenharPassaro(self, Tela):
        self.contagemDaImagem += 1
        if self.contagemDaImagem < self.TempoAnimacao:
            self.imagem = self.Imgs[0]
        elif self.contagemDaImagem < self.TempoAnimacao * 2:
            self.imagem = self.Imgs[1]
        elif self.contagemDaImagem < self.TempoAnimacao * 3:
            self.imagem = self.Imgs[2]
        elif self.contagemDaImagem < self.TempoAnimacao * 4:
            self.imagem = self.Imgs[1]
        elif self.contagemDaImagem < self.TempoAnimacao * 5:
            self.imagem = self.Imgs[0]
            self.contagemDaImagem = 0

        if self.angulo < -80:
            self.imagem = self.Imgs[1]
            self.contagemDaImagem = self.TempoAnimacao * 2

        ImagemPassaroRotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        PosicaoCentralImagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        RetanguloPassaro = ImagemPassaroRotacionada.get_rect(center=PosicaoCentralImagem)
        Tela.blit(ImagemPassaroRotacionada, RetanguloPassaro.topleft)

    def GetMask(self):
        return pygame.mask.from_surface(self.imagem)

# Todas as informações e métodos dos canos
class Cano:
    DistanciaVerticalCanos = 200
    VelocidadeCanos = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posicaoDoTopo = 0
        self.posicaoDaBase = 0
        self.imagemCanoDoTopo = pygame.transform.flip(ImagemCano, False, True)
        self.imagemCanoDaBase = ImagemCano
        self.CanoPassado = False
        self.DefinirAltura()

    def DefinirAltura(self):
        self.altura = random.randrange(50, 450)
        self.posicaoDoTopo = self.altura - self.imagemCanoDoTopo.get_height()
        self.posicaoDaBase = self.altura + self.DistanciaVerticalCanos

    def MoverCanos(self):
        self.x -= self.VelocidadeCanos

    def DesenharCanos(self, Tela):
        Tela.blit(self.imagemCanoDoTopo, (self.x, self.posicaoDoTopo))
        Tela.blit(self.imagemCanoDaBase, (self.x, self.posicaoDaBase))

    def ColisaoCano(self, Passarinho):
        MascaraDoPassaro = Passarinho.GetMask()
        MascaraCanoDoTopo = pygame.mask.from_surface(self.imagemCanoDoTopo)
        MascaraCanoDaBase = pygame.mask.from_surface(self.imagemCanoDaBase)

        DistanciaEntrePassarinhoTopo = (self.x - Passarinho.x, self.posicaoDoTopo - round(Passarinho.y))
        DistanciaEntrePassarinhoBase = (self.x - Passarinho.x, self.posicaoDaBase - round(Passarinho.y))

        ColisaoComTopo = MascaraDoPassaro.overlap(MascaraCanoDoTopo, DistanciaEntrePassarinhoTopo)
        ColisaoComBase = MascaraDoPassaro.overlap(MascaraCanoDaBase, DistanciaEntrePassarinhoBase)

        return ColisaoComTopo or ColisaoComBase

# Todas as informações e métodos do chão
class Chao:
    VelocidadeChao = 5
    LarguraChao = ImagemChao.get_width()
    ImagemClasseChao = ImagemChao

    def __init__(self, y):
        self.y = y
        self.xChao1 = 0
        self.xChao2 = self.LarguraChao

    def MoverChao(self):
        self.xChao1 -= self.VelocidadeChao
        self.xChao2 -= self.VelocidadeChao

        if self.xChao1 + self.LarguraChao < 0:
            self.xChao1 = self.xChao2 + self.LarguraChao
        if self.xChao2 + self.LarguraChao < 0:
            self.xChao2 = self.xChao1 + self.LarguraChao

    def DesenharChao(self, Tela):
        Tela.blit(self.ImagemClasseChao, (self.xChao1, self.y))
        Tela.blit(self.ImagemClasseChao, (self.xChao2, self.y))

# Desenha tudo o que for necessário na tela
def DesenharTudo(Tela, Passaros, Canos, Chao, Pontuacao):
    Tela.blit(ImagemFundo, (0, 0))
    
    for passaro in Passaros:  # Renomeado para 'passaro'
        passaro.DesenharPassaro(Tela)
    
    for cano in Canos:
        cano.DesenharCanos(Tela)

    Texto = FontePontuacao.render(f"Pontuação: {Pontuacao}", 1, (255, 255, 255))
    Tela.blit(Texto, (largura - 10 - Texto.get_width(), 10))
    
    Chao.DesenharChao(Tela)
    pygame.display.update()

# Função principal do jogo
def main():
    Passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    Pontuacao = 0
    Tela = pygame.display.set_mode((largura, altura))
    RelogioInterno = pygame.time.Clock()
    rodando = True

    while rodando:
        RelogioInterno.tick(30)
        
        # Evento de fechar o jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    Passaros[0].Pular()

        # Lógica dos canos
        removerCanos = []
        adicionarCano = False
        for cano in canos:
            for passaro in Passaros:  # Renomeado para 'passaro'
                if cano.ColisaoCano(passaro):
                    rodando = False

            if cano.x + cano.imagemCanoDoTopo.get_width() < 0:
                removerCanos.append(cano)

            if not cano.CanoPassado and cano.x < Passaros[0].x:
                cano.CanoPassado = True
                adicionarCano = True

            cano.MoverCanos()

        if adicionarCano:
            Pontuacao += 1
            canos.append(Cano(700))

        for cano in removerCanos:
            canos.remove(cano)

        for passaro in Passaros:  # Renomeado para 'passaro'
            if passaro.y + passaro.imagem.get_height() >= 730 or passaro.y < 0:
                rodando = False

        # Movimentação do pássaro
        for passaro in Passaros:  # Renomeado para 'passaro'
            passaro.MoverPassaro()

        DesenharTudo(Tela, Passaros, canos, chao, Pontuacao)

if __name__ == "__main__":
    main()