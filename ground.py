# Importando bibliotecas
import pygame

# Importando constantes
import const


# Classe do chão
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.load_image()  # Imagem
        self.rect = self.image.get_rect()  # Rect
        self.rect.x, self.rect.y = x, y  # Posição

    def update(self):
        """Atualiza a posição"""
        self.rect.x -= const.SCROLL_SPEED
        if self.rect.x <= -const.GROUND_WIDTH:
            self.kill()

    def load_image(self):
        """Carrega a imagem"""
        image = pygame.image.load("./data/assets/images/ground.png").convert()
        image = pygame.transform.scale(image, (const.GROUND_WIDTH, const.GROUND_HEIGHT))
        return image
