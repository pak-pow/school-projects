# AGUIRRE, PAUL VINCENT S.
# 1st Year Student
# CP 101 Computer Programming || Final Project


from os.path import join
from PIL import Image # Handle and resize images
from settings import *

class Menu:
    def __init__(self):
        # General setup
        self.display_surface = pygame.display.get_surface() # Drawing on the main game window
        self.font = pygame.font.Font(join('..', 'graphics', 'Russo_One.ttf'), 50) # getting the costom font and for rendering the text

        # Load and resize GIF frames
        self.bg_frames = self.load_gif(join('..', 'graphics', 'background.gif')) # Getting and Storing the frames of the animated GIF
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()

        # Menu options
        self.main_menu_options = ["START GAME", "INSTRUCTIONS", "OPTIONS", "QUIT"]
        self.pause_menu_options = ["RESUME", "MENU", "QUIT"]
        self.current_menu = "main" # Tracking the user to know whether the user is on the menu or the submenu
        self.current_option = 0
        self.volume = 100

    def load_gif(self, gif_path):
        # Load GIF frames, resize them, and convert to Pygame surfaces

        gif = Image.open(gif_path) # opens the gif file, resize, and convert to a format Pygame can display
        frames = []
        window_size = (self.display_surface.get_width(), self.display_surface.get_height())

        for frame in range(gif.n_frames):
            gif.seek(frame) # extracts every frame of the GIF
            resized_frame = gif.resize(window_size) # resizing the frame into windows size

            frame_surface = pygame.image.fromstring(
                resized_frame.tobytes(), resized_frame.size, resized_frame.mode
            ).convert()
            frames.append(frame_surface)
        return frames

    def draw_text(self, text, y, selected):
        # Draw text with dark outlines and shadows
        shadow_offset = 3
        outline_offset = 2
        color = "yellow" if selected else "white"

        # Creating a pygame surface containing the rendered text
        text_surface = self.font.render(text, True, color)

        # Drawing a rectangle to center the text
        text_rect = text_surface.get_rect(center=(self.display_surface.get_width() // 2, y))

        # creating the shadow effect for the text
        shadow_surface = self.font.render(text, True, "black")
        shadow_rect = text_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset

        # Creating an outline for the text
        outline_color = "black"
        for dx, dy in [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]:
            outline_surface = self.font.render(text, True, outline_color)
            outline_rect = text_rect.copy()
            outline_rect.x += dx
            outline_rect.y += dy
            self.display_surface.blit(outline_surface, outline_rect)

        # Drawing it onto the game screens
        self.display_surface.blit(shadow_surface, shadow_rect)
        self.display_surface.blit(text_surface, text_rect)

    def draw_text_with_font(self, text, y, font, selected):
        """Draw text with shadow, outline, and selected color."""
        shadow_offset = 3
        outline_offset = 2
        color = "yellow" if selected else "white"

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.display_surface.get_width() // 2, y))

        # Shadow
        shadow_surface = font.render(text, True, "black")
        shadow_rect = text_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset

        # Outline
        outline_color = "black"
        for dx, dy in [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]:
            outline_surface = font.render(text, True, outline_color)
            outline_rect = text_rect.copy()
            outline_rect.x += dx
            outline_rect.y += dy
            self.display_surface.blit(outline_surface, outline_rect)

        # Draw the shadow and the main text
        self.display_surface.blit(shadow_surface, shadow_rect)
        self.display_surface.blit(text_surface, text_rect)

    def animate_background(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:

            #keeps track of the current frame being displayed
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.last_update = current_time
        self.display_surface.blit(self.bg_frames[self.current_frame], (0, 0))

    def display_instructions(self):
        # Display the instructions screen with styled text over the animated background.
        running = True
        title_y = 50  # Starting Y position for the title
        line_spacing = 40  # Spacing between instruction lines
        title_font_size = 50  # Font size for the title
        content_font_size = 30  # Smaller font size for the content

        # Create the title font (larger size)
        title_font = pygame.font.Font(join('..', 'graphics', 'Russo_One.ttf'), title_font_size)
        # Create the content font (smaller size)
        content_font = pygame.font.Font(join('..', 'graphics', 'Russo_One.ttf'), content_font_size)

        while running:
            # Animate background
            self.animate_background()

            # Title (larger font size)
            self.draw_text_with_font("Instructions:", title_y, title_font, selected=False)

            # Instruction lines (smaller font size)
            instructions = [
                "Use arrow keys to move.",
                "Press UP to rotate.",
                "Press DOWN to speed up.",
                "Press ESC to pause.",
                "",
                "Press any key to return to the menu.",
                "",
                "Press ESC In-game to pause the game"
            ]
            for i, line in enumerate(instructions):
                y_position = title_y + 100 + i * line_spacing
                # Use the smaller content font for the instructions text
                self.draw_text_with_font(line, y_position, content_font, selected=False)

            pygame.display.update()  # Update the display

            # Event handling for returning to the menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    running = False  # Exit instructions screen

    def pause_menu(self, game, score, preview, next_shapes, play_music):
        #Display the in-game pause menu.

        selected_option = 0

        #Pauses the music when in pause menu
        pygame.mixer.music.pause()

        #creates a semi transparent screen for the pause menu
        overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))

        while True:
            # Render game components and semi-transparent overlay
            self.display_surface.fill(GRAY)
            self.display_surface.blit(game.surface, (PADDING, PADDING))
            pygame.draw.rect(self.display_surface, LINE_COLOR, game.rect, 2, 2)

            #displaying the score and the preview
            score.run()
            preview.run(next_shapes)

            # overlays the semiTransparent
            self.display_surface.blit(overlay, (0, 0))

            # Draw pause menu options
            for i, option in enumerate(self.pause_menu_options):
                color = "yellow" if i == selected_option else "white"
                text_surface = self.font.render(option, True, color)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 80))
                self.display_surface.blit(text_surface, text_rect)

            pygame.display.update()

            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(self.pause_menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(self.pause_menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Resume
                            pygame.mixer.music.unpause()
                            return "resume"
                        elif selected_option == 1:  # Back to Menu
                            pygame.mixer.music.stop()
                            play_music("menu")
                            return "menu"
                        elif selected_option == 2:  # Quit
                            pygame.quit()
                            exit()

    def run(self):

        # Handle the main menu loop and submenu navigation
        running = True

        while running:
            self.animate_background()  # Display animated background

            # Determine the current menu
            if self.current_menu == "main":
                menu_options = self.main_menu_options
            elif self.current_menu == "options":
                menu_options = [f"VOLUME: {self.volume}", "BACK"]

            # Display menu options
            spacing = 80
            start_y = self.display_surface.get_height() // 2 - len(menu_options) * spacing // 2
            for i, option in enumerate(menu_options):
                selected = (i == self.current_option)
                self.draw_text(option, start_y + i * spacing, selected)

            pygame.display.update()  # Update the screen

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.current_option = (self.current_option + 1) % len(menu_options)
                    elif event.key == pygame.K_UP:
                        self.current_option = (self.current_option - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        # Handle menu selections
                        if self.current_menu == "main":
                            if self.current_option == 0:  # START GAME
                                return "start_game"
                            elif self.current_option == 1:  # INSTRUCTIONS
                                return "instructions"
                            elif self.current_option == 2:  # OPTIONS
                                self.current_menu = "options"
                                self.current_option = 0
                            elif self.current_option == 3:  # QUIT
                                pygame.quit()
                                exit()
                        elif self.current_menu == "options":
                            if self.current_option == 0:  # Adjust volume
                                pass  # Volume adjustment happens with LEFT/RIGHT keys
                            elif self.current_option == 1:  # BACK
                                self.current_menu = "main"
                                self.current_option = 0
                    elif self.current_menu == "options" and event.key == pygame.K_LEFT:
                        # Adjust volume down
                        self.volume = max(0, self.volume - 10)
                        pygame.mixer.music.set_volume(self.volume / 100)
                    elif self.current_menu == "options" and event.key == pygame.K_RIGHT:
                        # Adjust volume up
                        self.volume = min(100, self.volume + 10)
                        pygame.mixer.music.set_volume(self.volume / 100)
