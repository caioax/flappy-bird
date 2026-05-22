# Importando bibliotecas
import pygame

# Importando constantes
import const


# Classe da tela game over
class Game_over:
    def __init__(self):
        self.buttons = []  # Lista com as imagens dos botões da tela game over
        self.rects = []  # Caixa de colisão dos botões
        self.load_images()  # Carregando imagens

        self.score = 0  # Pontuação
        self.best_score = const.DATA["score"]  # Melhor pontuação
        self.last_best_score = self.best_score  # Melhor pontuação anterior
        self.font = pygame.font.Font(
            "./data/assets/fonts/pixel.ttf", 27
        )  # Fonte da escrita
        self.new = False  # Controle do banner NEW

    def update(self, score, page, save_data):
        """Atualiza a pontução para a tela game over"""
        self.score = score
        if self.score > self.best_score:
            self.best_score = self.score
            save_data()
        if page == 3 and self.best_score > self.last_best_score:
            self.last_best_score = self.best_score
            self.new = True
        if page != 3:
            self.new = False

    def draw(self, screen):
        """Desenha elementos que compõem a tela"""
        gap = 30
        screen_width_half, screen_height_half = (
            const.SCREEN_WIDTH / 2,
            const.SCREEN_HEIGHT / 2,
        )
        result_width_haft, result_height_haft = (
            const.RESULT_WIDTH / 2,
            const.RESULT_HEIGHT / 2,
        )
        result_x, result_y = (
            screen_width_half - result_width_haft,
            screen_height_half - result_height_haft,
        )
        title_x, title_y = (
            screen_width_half - const.GAME_OVER_WIDTH / 2,
            result_y - const.GAME_OVER_HEIGHT - gap * 1.5,
        )

        screen.blit(self.title, (title_x, title_y))
        screen.blit(self.result, (result_x, result_y))

        score_value = self.font.render(str(self.score), True, pygame.Color(84, 56, 71))
        score_size = score_value.get_size()
        score_x, score_y = (
            result_x
            + result_width_haft
            - score_size[0]
            - (result_width_haft - score_size[0]) / 2
            + 10,
            result_y + 90,
        )
        screen.blit(score_value, (score_x, score_y))

        best_value = self.font.render(
            str(self.best_score), True, pygame.Color(84, 56, 71)
        )
        best_size = best_value.get_size()
        best_x, best_y = (
            result_x + result_width_haft + (result_width_haft - best_size[0]) / 2 - 10,
            result_y + 90,
        )
        screen.blit(best_value, (best_x, best_y))

        if self.new:
            new_x, new_y = (
                best_x + best_size[0] - const.NEW_WIDTH / 2,
                best_y + best_size[1] / 2,
            )
            screen.blit(self.new_image, (new_x, new_y))

        for i in range(2):
            button_x = (
                screen_width_half - const.GAME_OVER_BUTTON_WIDTH - gap / 2
                if i == 0
                else screen_width_half + gap / 2
            )
            button_y = const.RESULT_HEIGHT + result_y + gap
            self.rects[i].topleft = (button_x, button_y)
            screen.blit(self.buttons[i], (button_x, button_y))

    def load_images(self):
        """Carrega as imagens"""
        title = pygame.image.load("./data/assets/images/game_over.png").convert_alpha()
        self.title = pygame.transform.scale(
            title, (const.GAME_OVER_WIDTH, const.GAME_OVER_HEIGHT)
        )

        result = pygame.image.load("./data/assets/images/result.png").convert_alpha()
        self.result = pygame.transform.scale(
            result, (const.RESULT_WIDTH, const.RESULT_HEIGHT)
        )

        new = pygame.image.load("./data/assets/images/new.png").convert_alpha()
        new = pygame.transform.scale(new, (const.NEW_WIDTH, const.NEW_HEIGHT))
        self.new_image = pygame.transform.rotate(new, 20)

        buttons = pygame.image.load(
            "./data/assets/images/game_over_buttons.png"
        ).convert()
        for i in range(2):
            img = pygame.Rect(
                0,
                i * const.REAL_GAME_OVER_BUTTON_HEIGHT,
                const.REAL_GAME_OVER_BUTTON_WIDTH,
                const.REAL_GAME_OVER_BUTTON_HEIGHT,
            )
            button = buttons.subsurface(img)
            button = pygame.transform.scale(
                button, (const.GAME_OVER_BUTTON_WIDTH, const.GAME_OVER_BUTTON_HEIGHT)
            )
            rect = button.get_rect()
            self.buttons.append(button)
            self.rects.append(rect)
