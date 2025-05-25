# AGUIRRE, PAUL VINCENT S.
# 1st Year Student
# CP 101 Computer Programming || Final Project


from settings import *
from pygame.image import load
from os import path

class Preview:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface() # same with the score.py this refer to the main game screen where it will be drawn
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION)) # Drawing a blank canvas for the preview information
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING)) # Defining the position and the size of the said canvas

        # Shapes and a directory that loads an image for each tetromino from the folder
        self.shape_surfaces = {shape: load(path.join('..','Graphics',f'{shape}.png')).convert_alpha() for shape in TETROMINOS.keys()}

        # image position data
        self.increment_height = self.surface.get_height() / 3 # spliting the canvas into 3 section for displaying the next tetromino

    def display_pieces(self, shapes):
        # Displays the upcoming tetromino shapes on the preview area

        # loops through the shapes list
        for i, shape in enumerate(shapes):

            # getting the corresponding image
            shape_surface = self.shape_surfaces[shape]

            # positioning it like in the score.py. centered and spacing the image with increment
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height

            # displaying the image at the calculated position
            rect = shape_surface.get_rect(center = (x,y))
            self.surface.blit(shape_surface, rect)

    def run(self, next_shapes):

        # filling the canvas a color
        self.surface.fill(GRAY)

        # Displaying the upcoming pieces
        self.display_pieces(next_shapes)

        # DISPLAYING the preview area on the MAIN GAME SCREEN(right side)
        self.display_surface.blit(self.surface, self.rect)

        # Adding a white border around the canvas
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)