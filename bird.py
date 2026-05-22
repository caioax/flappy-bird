# Importando bibliotecas
import pygame

# Importando constantes
import const


# Classe do player
class Bird(pygame.sprite.Sprite):
    def __init__(self, skin="blue", rect_topleft=const.BIRD_POSITION_IN_MENU):
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe base Sprite

        self.skins = {  # Dicionário com todas skins disponíveis
            "blue": 0,
            "yellow": const.REAL_BIRD_HEIGHT,
            "red": 2 * const.REAL_BIRD_HEIGHT,
        }
        self.skin = skin if skin in self.skins else "blue"  # Skin atual

        self.sprites = []  # Lista com todos frames da sprite
        self.load_sprites()

        self.image = self.sprites[0]  # Imagem atual do pássaro
        self.rect = self.image.get_rect()  # Rect do pássaro
        self.rect.topleft = rect_topleft  # Posição inicial do sprite

        self.image_index = 0  # Índice do frame atual da animação voando
        self.vel = 0  # Controle da velocidade do pulo e da gravidade

        self.start_game = False  # Controle se o game foi iniciado
        self.alive = True  # Controle se o pássaro esta vivo

    def update(self):
        """Atualiza o estado do sprite"""
        self.flap_animation()
        self.gravity_and_flap()
        self.rotate()

    def toggle_skin(self, new_skin):
        """Troca de skin"""
        self.skin = new_skin
        self.load_sprites()

    def load_sprites(self):
        """Carrega as sprites"""
        self.sprites = []
        image = pygame.image.load(
            "./data/assets/images/birds_sprite.png"
        ).convert_alpha()
        for w in range(3):
            rect = pygame.Rect(
                w * const.REAL_BIRD_WIDTH,
                self.skins[self.skin],
                const.REAL_BIRD_WIDTH,
                const.REAL_BIRD_HEIGHT,
            )
            img = image.subsurface(rect)
            img = pygame.transform.scale(img, (const.BIRD_WIDTH, const.BIRD_HEIGHT))
            self.sprites.append(img)

    def flap_animation(self):
        """Atualiza animação voando"""
        if self.alive:
            self.image_index += 2
        if self.image_index >= 30:
            self.image_index = 0
        self.image = self.sprites[self.image_index // 10]

    def gravity_and_flap(self):
        """Gravidade e voou"""
        if self.start_game:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if (
                self.rect.y
                < const.SCREEN_HEIGHT - const.GROUND_HEIGHT - const.BIRD_HEIGHT / 2
            ):
                self.rect.y += int(self.vel)

    def start_jump(self):
        """Inicia o pulo"""
        if not self.start_game:
            self.start_game = True
        if self.rect.y > 0 and self.alive:
            self.vel = -8

    def rotate(self):
        """Rotação do pássaro"""
        if self.alive:
            self.image = pygame.transform.rotate(self.image, self.vel * -6)

    def restart_game(self, pos):
        """Reinicia o jogo"""
        self.rect.topleft = pos
        self.alive = True
        self.start_game = False
        self.vel = 0
