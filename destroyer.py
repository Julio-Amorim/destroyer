import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA_TELA, ALTURA_TELA = 800, 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Destroyer")

# Configurações de cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Configurações do jogo
FPS = 60
VELOCIDADE_FOGUETE = 10
VELOCIDADE_METEORO = 4
TEMPO_EXPLOSAO = 0.5  # Tempo em segundos para exibir explosões

# Carregar imagens
imagem_foguete = pygame.image.load('./assets/2.png')
imagem_meteoro = pygame.image.load('./assets/3.png')
imagem_explosao = pygame.image.load('./assets/4.png')

# Escalar imagens para melhor ajuste
imagem_foguete = pygame.transform.scale(imagem_foguete, (75, 75))
imagem_meteoro = pygame.transform.scale(imagem_meteoro, (50, 50))
imagem_explosao = pygame.transform.scale(imagem_explosao, (50, 50))

# Carregar quadros do GIF como uma lista de imagens
quadros_fundo = [
    pygame.image.load(f'./assets/gif/frame_{i}.png') for i in range(2, 101)
]
quadro_atual = 0  # Índice do quadro atual
atraso_quadro = 100  # Tempo entre quadros em milissegundos
ultima_atualizacao_quadro = pygame.time.get_ticks()

# Classes
class Foguete:
    def __init__(self):
        self.x = LARGURA_TELA // 2 - 25
        self.y = ALTURA_TELA - 70
        self.largura = 50
        self.altura = 50
        self.velocidade = VELOCIDADE_FOGUETE

    def desenhar(self):
        tela.blit(imagem_foguete, (self.x, self.y))

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.x < LARGURA_TELA - self.largura:
            self.x += self.velocidade

class Meteoro:
    def __init__(self):
        self.x = random.randint(0, LARGURA_TELA - 50)
        self.y = -50
        self.largura = 50
        self.altura = 50

    def mover(self):
        self.y += VELOCIDADE_METEORO

    def desenhar(self):
        tela.blit(imagem_meteoro, (self.x, self.y))

class Explosao:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tempo_inicio = time.time()

    def desenhar(self):
        tela.blit(imagem_explosao, (self.x, self.y))

# Função principal
def principal():
    global quadro_atual, ultima_atualizacao_quadro

    relogio = pygame.time.Clock()
    rodando = True
    fim_de_jogo = False

    # Inicializar objetos do jogo
    foguete = Foguete()
    meteoros = []
    explosoes = []
    vidas = 3
    tempo_jogo = 0

    # Timer para adicionar meteoros
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Evento para criar meteoros a cada 1 segundo

    while rodando:
        relogio.tick(FPS)
        tempo_atual = pygame.time.get_ticks()

        # Atualizar o quadro do fundo (animação do GIF)
        if tempo_atual - ultima_atualizacao_quadro > atraso_quadro:
            quadro_atual = (quadro_atual + 1) % len(quadros_fundo)
            ultima_atualizacao_quadro = tempo_atual

        # Exibir fundo animado
        tela.blit(quadros_fundo[quadro_atual], (0, 0))

        # Exibir vidas e tempo
        fonte = pygame.font.Font(None, 36)
        minutos = tempo_jogo // (FPS * 60)
        segundos = (tempo_jogo // FPS) % 60
        tempo_exibicao = fonte.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, BRANCO)
        vidas_exibicao = fonte.render(f"Vidas: {vidas}", True, BRANCO)
        tela.blit(tempo_exibicao, (10, 10))
        tela.blit(vidas_exibicao, (10, 50))

        if fim_de_jogo:
            # Exibir mensagem de fim de jogo
            texto_fim_de_jogo = fonte.render("Fim de jogo", True, VERMELHO)
            tela.blit(texto_fim_de_jogo, (LARGURA_TELA // 2 - 100, ALTURA_TELA // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        # Eventos do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.USEREVENT:  # Adicionar novo meteoro
                meteoros.append(Meteoro())

        # Movimentar foguete
        teclas = pygame.key.get_pressed()
        foguete.mover(teclas)

        # Atualizar meteoros
        for meteoro in meteoros[:]:
            meteoro.mover()
            if meteoro.y > ALTURA_TELA:  # Remover meteoros fora da tela
                meteoros.remove(meteoro)
            elif (foguete.x < meteoro.x + meteoro.largura and
                  foguete.x + foguete.largura > meteoro.x and
                  foguete.y < meteoro.y + meteoro.altura and
                  foguete.y + foguete.altura > meteoro.y):  # Colisão
                vidas -= 1
                explosoes.append(Explosao(meteoro.x, meteoro.y))
                meteoros.remove(meteoro)
                if vidas <= 0:
                    fim_de_jogo = True

        # Atualizar explosões
        for explosao in explosoes[:]:
            if time.time() - explosao.tempo_inicio > TEMPO_EXPLOSAO:
                explosoes.remove(explosao)

        # Desenhar objetos
        foguete.desenhar()
        for meteoro in meteoros:
            meteoro.desenhar()
        for explosao in explosoes:
            explosao.desenhar()

        # Atualizar tempo do jogo
        tempo_jogo += 1
        if tempo_jogo // FPS >= 40:  # Fim do jogo após 40 segundos
            fim_de_jogo = True

        # Atualizar tela
        pygame.display.flip()

    pygame.quit()

# Iniciar jogo
if __name__ == "__main__":
    principal()
