# AGUIRRE, PAUL VINCENT S.
# 1st Year Student
# CP 101 Computer Programming || Final Project


from settings import *
from os.path import join

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH,GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING)) # Draws a blank canvas for the score information
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING)) # Defininng the position and size of the said canvas
        self.display_surface = pygame.display.get_surface() # it will refer to the main game window where the score will be drawn

        # font
        self.font = pygame.font.Font(join('..','graphics','Russo_One.ttf'), 30) # creating a custom font, and its size

        #increment
        self.increment_height = self.surface.get_height() / 3   # splitting the score window into a 3 section

        # data
        self.score = 0
        self.level = 1
        self. lines = 0


    def display_text(self, pos, text):

        # rendering the text to text = ('Score', 1) into Score: 1
        text_surface = self.font.render(f'{text[0]}: {text[1]}', True, 'white')

        # making sure the position is centered
        text_rect = text_surface.get_rect(center = pos)

        # basically adding the text to the canvas
        self.surface.blit(text_surface, text_rect)

    def run(self):
        # Displaying the canvas and updating it

        # it first fills the canvas with the color
        self.surface.fill(GRAY)

        # Loops through the data
        for i, text in enumerate([('Score', self.score), ('Level', self.level), ('Lines', self.lines)]):
            x = self.surface.get_width() / 2 # Center Horizontally
            y = self.increment_height / 2 + i * self.increment_height # Spaces Vertically

            # using display to draw the text on the canvas
            self.display_text((x,y), text)

        # drawing the canvas onto the main display which is the game screen at the position specified by self.rect
        self.display_surface.blit(self.surface, self.rect)

        # adds the white border for apperance
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)