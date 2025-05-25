# AGUIRRE, PAUL VINCENT S.
# 1st Year Student
# CP 101 Computer Programming || Final Project

from settings import *
from sys import exit
from os.path import join

# components
from game import Game
from score import Score
from preview import Preview
from menu import Menu

from random import choice

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("TETRIS  ")

        self.state = "menu"

        # Components
        self.menu = Menu()
        self.game = None
        self.score = Score()
        self.preview = Preview()

        self.next_shapes = [choice(list(TETROMINOS.keys())) for _ in range(3)]

        self.menu_music = join('..', 'Sound', 'music.wav')
        self.game_music = join('..', 'Sound', 'in_game_sound.mp3')

        self.play_music("menu")

    def play_music(self, state):
        if state == "menu":
            pygame.mixer.music.load(self.menu_music)
        elif state == "game":
            pygame.mixer.music.load(self.game_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def initialize_game(self):
        self.game = Game(self.get_next_shape, self.update_score)
        self.play_music("game")

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            if self.state == "menu":
                result = self.menu.run()
                if result == "start_game":
                    self.initialize_game()
                    self.state = "game"
                elif result == "instructions":
                    self.menu.display_instructions()  # Show instructions screen
                elif result == "quit":
                    pygame.quit()
                    exit()
            elif self.state == "game":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            result = self.menu.pause_menu(
                                self.game,
                                self.score,
                                self.preview,
                                self.next_shapes,
                                self.play_music)
                            if result == "menu":
                                self.state = "menu"

                self.display_surface.fill(GRAY)
                self.game.run()
                self.score.run()
                self.preview.run(self.next_shapes)
                pygame.display.update()
                self.clock.tick(60)



if __name__ == '__main__':
    main = Main()
    main.run()
