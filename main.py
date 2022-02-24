from turtle import position
import pygame
from sys import exit

from pygame import QUIT

# tamanho da tela
x_tam = 1200
y_tam = 700
pygame.init()
tela = pygame.display.set_mode((x_tam, y_tam), 0)

#carregamento das imagens:
image_sshet_fundo = pygame.image.load("./assets/blocos.jpg").convert_alpha()
image_sshet_blocks = pygame.image.load("./assets/blocks.png").convert_alpha()
image_sshet_carac = pygame.image.load("./assets/manblack (1).png").convert_alpha()

imagem_fundo = pygame.image.load("./assets/city.gif").convert_alpha()
imagem_fundo = pygame.transform.scale(imagem_fundo,(x_tam,y_tam)) #conversão do tamanho da imagem de fundo

# matriz criada para desenhar na tela.

matriz = [
    "...................................................................",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "..................................................................p",
    "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu",
]

# Função criada para carregar as imagens nos sprites e na matriz
def get_img_by_gid(spritesheet, gid, columns=10, w=43, h=45, sh=3, sv=0, magenl=-30, margent=0):
    linha = gid // columns
    coluna = gid % columns
    x = magenl + (coluna * (w + sh))
    y = margent + (linha * (h + sv))
    return spritesheet.subsurface((x, y), (w, h))


img_plataforma = get_img_by_gid(image_sshet_fundo, 42)
img_grass = get_img_by_gid(image_sshet_blocks,5)

#função para transpor a matriz criada, na tela.

def pintar_linha(linha, conteudo):
    for coluna, caracter in enumerate(conteudo):
        x = coluna * img_plataforma.get_width()
        y = linha * img_plataforma.get_height()
        if caracter == "p":    # se o caracter da matriz for "p", a tela é preenchida naquele local com uma imagem, selecionada pelo gid.
            tela.blit(img_plataforma, (x, y))
        elif caracter == '.': # se o carcter for ".' , nada acontece por enquanto
            pass

        if caracter == "u":
            tela.blit(img_grass,(x,y))


def pintar_cenario():
    for linha, conteudo_linha in enumerate(matriz):
        pintar_linha(linha, conteudo_linha)

# personagem principal do game
class player(pygame.sprite.Sprite):
    def __init__(self):
        x_pos = 100
        y_pos = 515
        pygame.sprite.Sprite.__init__(self)
        self.ciclo_p = 50
        self.ciclo_c= 0
        self.indice = 0
        self.and_direita=[1,2,3]
        self.and_parado = [1]
        self.and_equerda=[4,5,6]
        self.frames = self.and_parado
        self.image = self.get_img(1)
        self.rect = pygame.Rect((x_pos,y_pos), (128, 128))
        self.pulo= False
        self.pos_y_ini = y_pos

    def get_img(self, gid):
        img = get_img_by_gid(spritesheet=image_sshet_carac, gid=gid, columns=1, w=128, h=128, sh=0, sv=0, magenl=0,
                             margent=-128)
        return img
    def pular(self):
        self.pulo = True

    def update(self):
        if self.pulo == True:
         if self.rect.y < 350:
            self.pulo = False
         self.rect.y -= 2
        else:
            if self.rect.y < self.pos_y_ini:
                self.rect.y += 2
            else:
             self.rect.y = self.pos_y_ini


        self.ciclo_c +=1
        if self.ciclo_c > self.ciclo_p:
           self.ciclo_c = 0
           self.indice += 1
        if self.indice >= len(self.frames):
            self.indice=0
        gid = self.frames[self.indice]
        self.image = self.get_img(gid)

        #movimento
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 1
            self.frames = self.and_equerda = [4,5,6]
        if key[pygame.K_RIGHT]:
            self.rect.x += 1
            self.frames = self.and_direita = [1, 2, 3]
        if key[pygame.K_SPACE]:
            if player1.rect.y != player1.pos_y_ini:
                pass
            else:
                self.pular()


           

player1 = player()
players = pygame.sprite.Group(player1)

while True: #laço de repetição para o game rodar, enquanto não for clicado em fechar.
    # calcular as regras:
    players.update()

    # pintar a tela:

    tela.fill((0,0,0))
    tela.blit(imagem_fundo, (0, 0))
    pintar_cenario()
    players.draw(tela)
    pygame.display.update()

    # captura_evebtos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
