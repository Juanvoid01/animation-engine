#instruction_step.py

import pygame
from objects.object import Object
from utils.colors import *
from enum import Enum, auto
from utils.rounded_rect import draw_rounded_rect

class Instruction_step(Object):
    """An Instruction_Step is an square with a color (green, red or gray)"""

    class State(Enum):
        NOT_EXECUTED = auto()
        EXECUTING = auto()
        EXECUTED = auto()
        ERROR = auto()


    EXECUTING_VELOCITY = 10
    BORDER_COLOR = COLOR_DARK_BLUE
    BORDER_WIDTH = 5
    BORDER_RADIUS = 3

    def __init__(self, posX, posY, width):
        """
        Initialize the Square.

        Args:
            posX (int): The x-coordinate of the top-left corner.
            posY (int): The y-coordinate of the top-left corner.
            width (int): The width of the square
        """
        super().__init__(posX, posY, width, width)

        self.state_colors = {
            self.State.NOT_EXECUTED: COLOR_GRAY,
            self.State.EXECUTED: COLOR_LIME_GREEN,
            self.State.ERROR: COLOR_RED
        }

        self.state = self.State.NOT_EXECUTED
        self.executed_percentage = 0
        self.state_executed_animation = 0 

    def reset(self):
        """
        Reset object to default state
        """
        self.state = self.State.NOT_EXECUTED
        self.executed_percentage = 0




        self.state_executed_animation = 0 


    def update(self, tick):
        """
        Update the state of the square.
        For now, it does nothing, but you can extend it to add animations or interactions.
        
        Args:
            tick (int): The current tick of the game (used for animations, etc.).
        """
        if self.state == self.State.EXECUTING:
            if self.executed_percentage >= 100:
                self.state = self.State.EXECUTED
                self.state_executed_animation = 0 
            else:
                self.executed_percentage += self.EXECUTING_VELOCITY
        elif self.state == self.State.EXECUTED:
            if self.state_executed_animation == 0:
                if self.executed_animation() == True:
                    self.state_executed_animation = 1
                

    def draw(self, screen):
        """
        Draw the square on the given screen.

        Args:
            screen (pygame.screen): The screen to draw the square on.
        """
        # Draw the black border
        rounded_rect = (self.posX - self.BORDER_WIDTH, self.posY - self.BORDER_WIDTH, self.sizeX + 2*self.BORDER_WIDTH, self.sizeY + 2*self.BORDER_WIDTH)

        draw_rounded_rect(screen, rounded_rect, self.BORDER_COLOR, self.BORDER_RADIUS)

        if self.state == self.State.NOT_EXECUTED:
            pygame.draw.rect(
                screen,
                self.state_colors.get(self.State.NOT_EXECUTED, COLOR_GRAY),
                (self.posX, self.posY, self.sizeX, self.sizeY)
            )
        if self.state == self.State.EXECUTED:

            pygame.draw.rect(
                screen,
                self.state_colors.get(self.State.EXECUTED, COLOR_GRAY),
                (self.posX, self.posY, self.sizeX, self.sizeY)
            )

        elif self.state == self.State.ERROR:
            pygame.draw.rect(
                screen,
                self.state_colors.get(self.State.ERROR, COLOR_GRAY),
                (self.posX, self.posY, self.sizeX, self.sizeY)
            )
        elif self.state == self.State.EXECUTING:
            # Draw the inside color, first the not executed and then the executed color
            not_executed_width = self.sizeX * (100-self.executed_percentage)/100
            executed_width = self.sizeX * self.executed_percentage/100
            pygame.draw.rect(
                screen,
                self.state_colors.get(self.State.NOT_EXECUTED, COLOR_GRAY),
               (self.posX + executed_width, self.posY, not_executed_width, self.sizeY)
            )
            pygame.draw.rect(
                screen,
                self.state_colors.get(self.State.EXECUTED, COLOR_GRAY),
                (self.posX, self.posY, executed_width, self.sizeY)
            )

    def start_execution(self):
        """Start executing the step."""
        if self.state == self.State.NOT_EXECUTED:
            self.state = self.State.EXECUTING
            self.executed_percentage = 0
    
    def execution_error(self):
        """Mark the step as an error if not already executed."""
        if self.state in {self.State.EXECUTED, self.State.EXECUTING}:
            self.state = self.State.ERROR

    def is_executed(self):
        """Return True if the step is executed."""
        return self.state == self.State.EXECUTED    
    
    def executed_animation(self):
        """
        First increment the size to 1.5 times the original size, then decrement back to the original size.
        Repeats a second time with a target size of 1.3 times the original size.

        Returns:
            bool: True if the object has completed the animation, False otherwise.
        """

        if not hasattr(self, "_executed_animation_stage"):
            self._executed_animation_stage = 0
            self._original_size = self.sizeX  

        # Increment/Decrement logic based on the current stage
        if self._executed_animation_stage == 0:
            # Increment to 1.5x size
            target_size = self._original_size * 1.5

            if self.change_size(delta_size=3, target_width=target_size, target_height=target_size, maintain_center=True):
                self._executed_animation_stage = 1

        elif self._executed_animation_stage == 1:
            # Decrement back to original size
            target_size = self._original_size

            if self.change_size(delta_size=3, target_width=target_size, target_height=target_size, maintain_center=True):
                self._executed_animation_stage = 2

        elif self._executed_animation_stage == 2:
            # Increment to 1.3x size
            target_size = self._original_size * 1.3

            if self.change_size(delta_size=3, target_width=target_size, target_height=target_size, maintain_center=True):
                self._executed_animation_stage = 3

        elif self._executed_animation_stage == 3:
            # Decrement back to original size
            target_size = self._original_size

            if self.change_size(delta_size=3, target_width=target_size, target_height=target_size, maintain_center=True):
                self._executed_animation_stage = 4

        elif self._executed_animation_stage == 4:
            # Animation is complete, clean up attributes
            del self._executed_animation_stage
            del self._original_size
            return True

        # Animation is still running
        return False




