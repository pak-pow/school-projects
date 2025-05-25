# AGUIRRE, PAUL VINCENT S.
# 1st Year Student
# CP 101 Computer Programming || Final Project


from pygame.time import get_ticks
import pygame.time


class Timer:
    def __init__(self, duration, repeated = False, func = None):

        # calls the timer whether to repeat it
        self.repeated = repeated

        # calling a function when the timer is finished
        self.func = func

        # it is the duration or how long the timer has started
        self.duration = duration

        # tracks the timer when it starts
        self.start_time = 0

        #indicating whether the timer is running or not
        self.active = False

    def activate(self):

        # marks the timer as running
        self.active = True

        # getting the current time in MILLISECOND since the game has started
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):

        # marks the timer to stop
        self.active = False

        # clears the time to marks its end
        self.start_time = 0

    def update(self):

        # getting the time in millisecond
        current_time = pygame.time.get_ticks()

        # compare it to make sure the timer is active before procceding
        if current_time - self.start_time >= self.duration and self.active:

            # Call a function
            if self.func and self.start_time != 0:
                self.func()

            # reset timer
            self.deactivate()

            # repeat the timer
            if self.repeated:
                self.activate()