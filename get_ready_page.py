# Importando bibliotecas
import pygame

# Importando constantes
import const


# Classe da tela get ready
class Get_ready:
    def __init__(self):
        self.load_images()  # Carregando imagens

    def draw(self, screen):
        """Desenha elementos que compõem a tela"""
        screen.blit(
            self.title, (const.SCREEN_WIDTH / 2 - const.GET_READY_WIDTH / 2, 200)
        )
        screen.blit(
            self.tap_image,
            (
                const.SCREEN_WIDTH / 2 - const.TAP_WIDTH / 2,
                const.SCREEN_HEIGHT / 2 - const.TAP_HEIGHT / 2,
            ),
        )

    def load_images(self):
        """Carrega as imagens"""
        title = pygame.image.load("./data/assets/images/get_ready.png").convert_alpha()
        self.title = pygame.transform.scale(
            title, (const.GET_READY_WIDTH, const.GET_READY_HEIGHT)
        )

        tap_image = pygame.image.load("./data/assets/images/tap.png").convert_alpha()
        self.tap_image = pygame.transform.scale(
            tap_image, (const.TAP_WIDTH, const.TAP_HEIGHT)
        )
