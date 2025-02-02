#instruction.py

import pygame
from objects.instruction_step import Instruction_step
from objects.object import Object
from enum import Enum, auto

class Instruction(Object):
    """An instruction object with 5 instruction_steps represented as squares."""

    class State(Enum):
        NOT_EXECUTED = auto()
        EXECUTING = auto()
        EXECUTED = auto()
        ERROR = auto()

    NUM_STEPS = 5  # Number of steps in the instruction

    def __init__(self, posX, posY, width):
        """
        Initialize the Square.

        Args:
            posX (int): The x-coordinate of the top-left corner.
            posY (int): The y-coordinate of the top-left corner.
            width (int): The width of the instruction rectangle
        """
        super().__init__(posX, posY, width, width)

        self.state = self.State.NOT_EXECUTED
        self.step_executing = 0
        self.instruction_steps = []

        step_width = self.get_step_width()
        for i in range(self.NUM_STEPS):
            step_posX = posX + i * step_width
            self.instruction_steps.append(Instruction_step(step_posX, posY, step_width))

    def reset(self):
        """
        Reset object to default state
        """
        self.state = self.State.NOT_EXECUTED
        self.step_executing = 0
        for i in range(self.NUM_STEPS):
             self.instruction_steps[i].reset()

    def align_position_of_childs(self):
        """
        Update the position of all the child objects
        """
        step_width = int(self.sizeX / self.NUM_STEPS)
        for i in range(self.NUM_STEPS):
            step_posX = self.posX + i * step_width
            self.instruction_steps[i].set_pos(step_posX,self.posY)

    def move(self, deltaX, deltaY):
        """Move the object by deltaX and deltaY."""
        super().move(deltaX, deltaY)

        self.align_position_of_childs()


    def go_to(self, deltaX, deltaY, finalX, finalY):

        result = super().go_to(deltaX, deltaY, finalX, finalY)

        self.align_position_of_childs()
        
        return result

    def go_to_smooth(self, finalX, finalY, speed=5):

        result = super().go_to_smooth(finalX, finalY, speed)
        self.align_position_of_childs()
        
        return result

    
    def update(self, tick):
        """Update logic for the instruction."""

        if self.state == self.State.EXECUTING:

            if self.instruction_steps[self.step_executing].is_executed():
                self.step_executing +=1
            else:
                self.instruction_steps[self.step_executing].start_execution()
            
            if self.step_executing >= self.NUM_STEPS:
                self.state = self.State.EXECUTED

        for step in self.instruction_steps:
            step.update(tick)
    
        

    def draw(self, screen):
        """Draw the instruction on the screen."""
        for step_square in self.instruction_steps:
            step_square.draw(screen)

    def start_execution(self):
        """
        Starts executing the instruction

        """
        if self.state == self.State.NOT_EXECUTED:
            self.state = self.State.EXECUTING
            self.step_executing = 0

    
    def execution_error(self):
        """
        Stops executing the instruction

        """
        self.state = self.State.ERROR

        for step_square in self.instruction_steps:
            step_square.execution_error()

    def is_executed(self):
        """Return True if the step is executed."""
        return self.state == self.State.EXECUTED   
    
    def get_step_width(self):
        """Return the witdth of each step (sizeX / NUM_STEP)"""
        return int(self.sizeX / self.NUM_STEPS)
    
    def get_step_executing(self):        
        """Return the step that is currently executing"""
        return self.step_executing