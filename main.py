# Importando bibliotecas
import random
from sys import exit

import pygame

# Importando constantes
import const
# Importando classes
from background import Background
from bird import Bird
from game_over_page import Game_over
from get_ready_page import Get_ready
from ground import Ground
from menu_page import Menu
from pipe import Pipe


# Classe do jogo
class Game:
    def __init__(self):

        self.icon = pygame.image.load("./data/icon/icon.ico") # Icone do app

        self.background_color = (84, 192, 201) # Cor de fundo da tela
        self.fps = 60 # Taxa de quadros por segundo
        self.score = 0 # Pontuação

        self.start_game = False # Controle se o jogo começou
        self.pause = False # Controle do pause

        self.pages = { # Dicionário com todas as telas
            "menu": 0,
            "get_ready": 1,
            "game": 2,
            "game_over": 3,
        }
        self.musics = { # Dicionário com todas as músicas
            "menu": "menu_music.wav",
            "get_ready": "get_ready_music.wav",
            "game": "game_music.wav",
            "game_over": "game_over_music.wav"
        }

        self.page = self.pages["menu"] # Página atual

        self.flash = False # Controle do efeito de flash ao morrer
        self.flash_alpha = 0 # Opacidade do efeito de flash

    # Main
    def main(self):
        """ Inicia todo jogo """
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_icon(self.icon)
        const.load_data() # Carega dados salvos
        self.font = pygame.font.Font('./data/assets/fonts/pixel.ttf', 23)
        self.create_screen()
        self.start_elements()
        self.start_sounds()
        self.play_music(self.musics["menu"])
        self.game_loop()

    # Game
    def game_loop(self):
        """ Loop principal do jogo """
        run = True
        while run:
            self.events() # Eventos
            if not self.pause:
                # Pinta toda a tela para resetar o freme
                self.screen.fill(self.background_color)

                # Desenhando fundo
                self.background.draw(self.screen)

                # Gera mais chão
                self.spaw_ground()

                # Desenhando elementos
                self.draw_all()

                # Atualizando elementos
                self.update_all()

                # Detecta colisões
                self.collisions()

                # Gera canos
                self.spaw_pipes()

            self.draw_pause_icon() # Icone de pause
            self.clock.tick(self.fps) # Taxa de quadros por segundo
            pygame.display.update() # Atualizando tela

    def game_over(self):
        """ Ação ao perder o jogo """
        self.hit_sound.play()
        self.die_sound.play()
        self.bird.sprite.start_jump()
        self.bird.sprite.alive = False
        self.flash = True
        self.page = self.pages["game_over"]
        self.play_music(self.musics["game_over"])

    # Create
    def create_screen(self):
        """ Cria a tela """
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

    # Events
    def events(self):
        """ Verifica os eventos """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Eventos do teclado
            if event.type == pygame.KEYDOWN:
                # Tecla espaço
                if event.key == pygame.K_SPACE and self.page == self.pages["game"] or self.page == self.pages["get_ready"]:
                    self.event_jump()
                # Tecla p
                if event.key == pygame.K_p and self.start_game and self.bird.sprite.alive:
                    self.event_pause()
            
            # Eventos do Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Botão 1 (Botão esquerdo)
                # Tela game
                if event.button == 1 and self.pause_rect.collidepoint(event.pos) and self.page == self.pages["game"]:
                    self.event_pause()  
                elif event.button == 1 and self.page == self.pages["get_ready"] or self.page == self.pages["game"]:
                    self.event_jump()

                # Tela game over
                if event.button == 1 and self.game_over_page.rects[0].collidepoint(event.pos) and self.page == self.pages["game_over"]:
                    self.event_menu()
                elif event.button == 1 and self.game_over_page.rects[1].collidepoint(event.pos) and self.page == self.pages["game_over"]:
                    self.event_restart()
                
                # Tela menu
                if event.button == 1 and self.menu_page.play_rect.collidepoint(event.pos) and self.page == self.pages["menu"]:
                    self.event_play()
                elif event.button == 1 and self.menu_page.bird_rects_btn[0].collidepoint(event.pos) and self.page == self.pages["menu"]:
                    self.event_toggle_skin("blue")
                elif event.button == 1 and self.menu_page.bird_rects_btn[1].collidepoint(event.pos) and self.page == self.pages["menu"]:
                    self.event_toggle_skin("yellow")
                elif event.button == 1 and self.menu_page.bird_rects_btn[2].collidepoint(event.pos) and self.page == self.pages["menu"]:
                    self.event_toggle_skin("red")

    def event_play(self):
        """ Evento do botão play da tela menu """
        self.click_sound.play()
        self.bird.sprite.rect.center = const.BIRD_START_POSITION
        self.page = self.pages["get_ready"]
        self.play_music(self.musics["get_ready"])

    def event_jump(self):
        """ Evento de pulo """
        if not self.pause:
            self.wing_sound.play()
            if not self.start_game:
                self.page = self.pages["game"]
                self.play_music(self.musics["game"])
                self.start_game = True
            self.bird.sprite.start_jump()

    def event_menu(self):
        """ Evento do botão menu da tela game_over """
        self.click_sound.play()
        self.page = self.pages["menu"]
        self.play_music(self.musics["menu"])
        for pipe in self.pipes:
            pipe.kill()
        self.score = 0
        self.bird.sprite.restart_game(const.BIRD_POSITION_IN_MENU)
        self.start_game = False

    def event_restart(self):
        """ Evento do botão restart da tela game_over """
        self.click_sound.play()
        self.page = self.pages["get_ready"]
        self.play_music(self.musics["get_ready"])
        for pipe in self.pipes:
            pipe.kill()
        self.score = 0
        self.bird.sprite.restart_game(const.BIRD_START_POSITION)
        self.start_game = False

    def event_toggle_skin(self, new_skin):
        """ Evento de trocar a skin do menu """
        self.click_sound.play()
        self.bird.sprite.toggle_skin(new_skin)
        self.menu_page.toggle_skin(new_skin)
        self.save_data()

    def event_pause(self):
        """ Evento de pausar/despausar o jogo """
        self.click_sound.play()
        self.pause = not self.pause
        if self.pause: self.play_music(self.musics["get_ready"])
        else: self.play_music(self.musics["game"])

    # Draw
    def draw_all(self):
        """ Desenha tudo na tela """
        self.pipes.draw(self.screen)
        self.ground.draw(self.screen)
        self.bird.draw(self.screen)
        if self.page == self.pages["menu"]: self.menu_page.draw(self.screen)
        if self.page == self.pages["get_ready"]: self.get_ready_page.draw(self.screen)
        if self.page == self.pages["game_over"]: self.game_over_page.draw(self.screen)
        self.draw_flash()

        # Pontuação
        self.draw_score() 

    def draw_flash(self):
        """ Desenha efeito de flash quando morre """
        flash = pygame.Surface((const.SCREEN_WIDTH, const.SCREEN_HEIGHT), pygame.SRCALPHA)
        flash.fill((255, 255, 255, self.flash_alpha))
        self.screen.blit(flash, (0, 0))

    def draw_score(self):
        """ Desenha pontuação do player """
        if self.page == self.pages["game"]:
            score_text = self.font.render('Score: ' + str(self.score), True, pygame.Color(84, 56, 71))
            self.screen.blit(score_text, (30, 30))

    def draw_pause_icon(self):
        """ Desenha icon de pausar """
        if self.page == self.pages["game"]:
            i = 1 if self.pause else 0
            self.pause_icon = self.pause_images[i]
            self.screen.blit(self.pause_icon, (const.SCREEN_WIDTH - const.PAUSE_WIDTH - 20, 20))

    # Update
    def update_all(self):
        """ Atualiza tudo """
        if self.bird.sprite.alive:
            self.background.update()
            self.pipes.update()
            self.ground.update()
        self.bird.update()
        self.menu_page.update()
        self.game_over_page.update(self.score, self.page, self.save_data)
        self.flash_update()

    def flash_update(self):
        """ Atualiza efeito de flash """
        if self.flash:
            self.flash_alpha += 20
            if self.flash_alpha >= 255:
                self.flash_alpha = 255
                self.flash = False 
        else:
            self.flash_alpha -= 20
            if self.flash_alpha < 0: self.flash_alpha = 0

    def score_update(self):
        """ Incrementa uma unidade há pontuação """
        self.point_sound.play()
        self.score += 1

    # Spaw
    def spaw_ground(self):
        """ Gera chão infinito """
        if len(self.ground) <= 3:
            self.x_pos_ground = self.ground.sprites()[-1].rect.x + const.GROUND_WIDTH
            self.ground.add(Ground(self.x_pos_ground, self.y_pos_ground))
    
    def spaw_pipes(self):
        """ gera os canos """
        if self.pipe_timer <= 0 and self.start_game and self.bird.sprite.alive:
            margin = (-const.PIPE_HEIGHT + 70,
                        -const.PIPE_HEIGHT + const.SCREEN_HEIGHT - const.GROUND_HEIGHT - const.PIPES_GAP_Y - 70)
            x_top, x_bottom = const.SCREEN_WIDTH, const.SCREEN_WIDTH
            y_top = random.randint(margin[0], margin[1])
            y_bottom = y_top + const.PIPE_HEIGHT + const.PIPES_GAP_Y
            self.pipes.add(Pipe(x_top, y_top, self.score_update, direction="down"))
            self.pipes.add(Pipe(x_bottom, y_bottom, self.score_update, direction="up"))
            self.pipe_timer = const.PIPES_GAP_X
        self.pipe_timer -= 1

    # Collision
    def collisions(self):
        """ Verifica colisões """
        if self.bird.sprite.alive:
            collision_pipes = pygame.sprite.spritecollide(self.bird.sprites()[0], self.pipes, False)
            collision_ground = pygame.sprite.spritecollide(self.bird.sprites()[0], self.ground, False)
            if collision_pipes or collision_ground:
                self.game_over()

    # Save
    def save_data(self):
        # Salva informações
        with open("data.txt", "w") as file:
            file.write(f"score: {self.game_over_page.best_score}\n")
            file.write(f"skin: {self.bird.sprite.skin}")

    # Start
    def start_elements(self):
        """ Inicializa todos os elementos """
        # Inicializa classe do fundo
        self.background = Background()

        # Inicializando sprite do pássaro
        self.bird = pygame.sprite.GroupSingle()
        self.bird.add(Bird(const.DATA["skin"]))

        # Inicializando canos
        self.pipe_timer = 0
        self.pipes = pygame.sprite.Group()

        # Inicializando sprite do chão
        self.x_pos_ground, self.y_pos_ground = 0, const.SCREEN_HEIGHT - const.GROUND_HEIGHT
        self.ground = pygame.sprite.Group()
        self.ground.add(Ground(self.x_pos_ground, self.y_pos_ground))

        # Iniciando páginas
        self.menu_page = Menu()
        self.get_ready_page = Get_ready()
        self.game_over_page = Game_over()

        # Imagem pause
        self.pause_images = [] 
        pause_image = pygame.image.load("./data/assets/images/pause.png").convert()
        for i in range(2):
            rect = pygame.Rect(i * const.REAL_PAUSE_WIDTH, 0, const.REAL_PAUSE_WIDTH, const.REAL_PAUSE_HEIGHT)
            icon = pause_image.subsurface(rect)
            icon = pygame.transform.scale(icon, (const.PAUSE_WIDTH, const.PAUSE_HEIGHT))
            self.pause_images.append(icon)
        self.pause_icon = self.pause_images[0]
        self.pause_rect = self.pause_icon.get_rect()
        self.pause_rect.topleft = (const.SCREEN_WIDTH - const.PAUSE_WIDTH - 20, 20)
    
    def start_sounds(self):
        """ Inicia todos efeitos sonoros """
        self.click_sound = pygame.mixer.Sound("./data/assets/sounds/click.wav")
        self.die_sound = pygame.mixer.Sound("./data/assets/sounds/die.wav")
        self.hit_sound = pygame.mixer.Sound("./data/assets/sounds/hit.wav")
        self.point_sound = pygame.mixer.Sound("./data/assets/sounds/point.wav")
        self.wing_sound = pygame.mixer.Sound("./data/assets/sounds/wing.wav")

    # Play
    def play_music(self, music):
        """ Controla qual music esta tocando no momento """
        pygame.mixer.music.stop()
        pygame.mixer.music.load(f"./data/assets/musics/{music}")
        pygame.mixer.music.play(-1)

# Rodando o jogo
Game().main()
