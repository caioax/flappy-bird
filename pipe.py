# Importando bibliotecas
import pygame

# Importando constantes
import const

# Classe dos canos
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, score_update, direction="down"):
        pygame.sprite.Sprite.__init__(self)

        self.score_update = score_update # função que atuliza a pontuação
        self.direction = direction # Direção que o cano está virado (Para cima ou para baixo)
        self.enter, self.exit, self.passed = False, False, False # Variáveis de controle para verificar se o payer passou do cano

        self.image = self.load_image() # Imagem 
        self.rect = self.image.get_rect() # Rect
        self.rect.x, self.rect.y = x, y # Posição

    
    def update(self):
        """ Atualiza a posição e pontuação """
        self.rect.x -= const.SCROLL_SPEED
        if self.rect.x <= -const.PIPE_WIDTH:
            self.kill()
        
        # pontuação
        if self.direction == "down":
            if const.BIRD_START_POSITION[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if const.BIRD_START_POSITION[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                self.score_update()
    
    def load_image(self):
        """ Carrega a imagem """
        image = pygame.image.load("./data/assets/images/pipe.png").convert_alpha()
        if self.direction == "up":
            image = pygame.transform.flip(image, False, True)
        image = pygame.transform.scale(image, (const.PIPE_WIDTH, const.PIPE_HEIGHT))
        return image
        