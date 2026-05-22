# Importando bibliotecas
import pygame

# Importando classes
from bird import Bird

# Importando constantes
import const

# Classe da tela menu
class Menu:
    def __init__(self):

        # Dicionário de skins
        self.skins = {
            "blue": 0,
            "yellow": 1,
            "red": 2,
        }
        self.skin = const.DATA["skin"] # Skin atual

        # Texto de créditos
        gap = 20
        self.font = pygame.font.Font('./data/assets/fonts/pixel.ttf', 20)
        self.credits = self.font.render('Made by Caio, finished on 10/03/2025', True, pygame.Color(84, 56, 71))
        self.credits_size = self.credits.get_size()

        # Posições dos elementos
        self.title_x, self.title_y = const.SCREEN_WIDTH / 2 - const.FLAPPY_BIRD_WIDTH / 2, 150
        self.play_button_x, self.play_button_y = const.SCREEN_WIDTH / 2 - const.PLAY_BUTTON_WIDTH / 2, const.SCREEN_HEIGHT / 2 - const.PLAY_BUTTON_HEIGHT / 2
        self.credits_x, self.credits_y = const.SCREEN_WIDTH - self.credits_size[0] - gap, const.SCREEN_HEIGHT - self.credits_size[1] -  gap
        self.pos_birds_btn = [
            [const.SCREEN_WIDTH / 2 - const.BIRD_WIDTH * 3, self.play_button_y + const.PLAY_BUTTON_HEIGHT * 2],
            [const.SCREEN_WIDTH / 2 -  const.BIRD_WIDTH / 2, self.play_button_y + const.PLAY_BUTTON_HEIGHT * 2],
            [const.SCREEN_WIDTH / 2 + const.BIRD_WIDTH * 2, self.play_button_y + const.PLAY_BUTTON_HEIGHT * 2],
        ]

        self.load_images() # Carregando imagens
        self.load_birds() # Sprites de pássaros para butões

    def update(self):
        """ Atualiza botões de pássaros """
        self.birds_btn.update()

    def draw(self, screen):
        """ Desenha elementos que compõem a tela """
        screen.blit(self.title, (self.title_x, self.title_y))
        screen.blit(self.play_button, (self.play_button_x, self.play_button_y))            
        screen.blit(self.credits, (self.credits_x, self.credits_y))
        self.birds_btn.draw(screen)

        pos_x = self.pos_birds_btn[self.skins[self.skin]][0] - 10
        pos_y = self.pos_birds_btn[self.skins[self.skin]][1] - 10
        rect = pygame.Rect(pos_x, pos_y, const.BIRD_WIDTH + 20, const.BIRD_HEIGHT + 20)
        pygame.draw.rect(screen, (84, 56, 71), rect, width= 5, border_radius= 10)

    def toggle_skin(self, new_skin):
        """ Troca a skin selecionada """
        self.skin = new_skin

    def load_images(self):
        """ Carrega as imagens """
        title = pygame.image.load("./data/assets/images/flappy_bird.png").convert_alpha()
        self.title = pygame.transform.scale(title, (const.FLAPPY_BIRD_WIDTH, const.FLAPPY_BIRD_HEIGHT))       

        play_button = pygame.image.load("./data/assets/images/play_button.png").convert_alpha()
        self.play_button = pygame.transform.scale(play_button, (const.PLAY_BUTTON_WIDTH, const.PLAY_BUTTON_HEIGHT))
        self.play_rect = self.play_button.get_rect()
        self.play_rect.topleft = (self.play_button_x, self.play_button_y)
    
    def load_birds(self):
        """ Carrega sprites de pássaros para botões """
        self.birds_btn = pygame.sprite.Group()
        self.bird_rects_btn = []

        for i, pos in enumerate(self.pos_birds_btn):
            skin = "blue" if i == 0 else "yellow" if i == 1 else "red"
            bird = Bird(skin, pos)
            rect = pygame.Rect(pos[0] -5, pos[1] -5, const.BIRD_WIDTH + 10, const.BIRD_HEIGHT + 10)
            self.bird_rects_btn.append(rect)
            self.birds_btn.add(bird)


