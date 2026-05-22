# Importando bibliotecas
import pygame

# Importando constantes
import const

# Classe do fundo
class Background:
    def __init__(self):

        self.images = [] # Lista com todas as imagens
        self.load_images()

        self.positions_x = [] # Lista com todas as posições no eixo X
        self.load_positions_x()

    def load_positions_x(self):
        """ Posições iniciais no eixo X das imagens """
        for _ in range(len(self.images)):
            self.positions_x.append([0, const.SCREEN_WIDTH])
    
    def load_images(self):
        """ Carrega as imagens """
        image = pygame.image.load("./data/assets/images/background.png").convert_alpha()
        for h in range(2):
            for w in range(2):
                rect = pygame.Rect(w * const.REAL_BACKGROUND_WIDTH, h * const.REAL_BACKGROUND_HEIGHT, const.REAL_BACKGROUND_WIDTH, const.REAL_BACKGROUND_HEIGHT)
                img = image.subsurface(rect)
                img = pygame.transform.scale(img, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
                self.images.append(img)

    def update(self):
        """ Atualiza a posição """
        for i, pos in enumerate(reversed(self.positions_x)):
            speed = const.SCROLL_SPEED - (i + 2) / 2
            if speed <= 0:
                speed = 0
            pos[0] -= speed
            pos[1] -= speed
            
            # Volta imagem para a direita quando ela some do lado esquerdo
            if pos[0] <= -const.SCREEN_WIDTH:
                pos[0] += 2 * const.SCREEN_WIDTH
            elif pos[1] <= -const.SCREEN_WIDTH:
                pos[1] += 2 * const.SCREEN_WIDTH

    def draw(self, screen):
        """ Desenha na tela """
        for i, img in enumerate(self.images):
            screen.blit(img, (self.positions_x[i][0], 0))
            screen.blit(img, (self.positions_x[i][1], 0))

