#scene_instructions.py

from objects.instruction import Instruction
from scene.scene import Scene
from enum import Enum, auto

class SceneInstructions(Scene):
    """SceneInstructions"""

    class State(Enum):
        MOVE1 = auto()
        EXECUTE1 = auto()
        JIGGLE = auto()
        MOVE2 = auto()
        EXECUTE2 = auto()
        FINISHED = auto()

    MOVE_SPEED = 60
    EXECUTION_SPEED = 20
    NUM_INSTRUCTIONS = 5
    INSTRUCTION_WIDTH = 200

    def __init__(self):
        super().__init__()

        self.state = self.State.MOVE1

        self.instructions = []

        self.instructions.append(Instruction(2000,200,self.INSTRUCTION_WIDTH,self.EXECUTION_SPEED))
        self.instructions.append(Instruction(2000,300,self.INSTRUCTION_WIDTH,self.EXECUTION_SPEED))
        self.instructions.append(Instruction(2000,400,self.INSTRUCTION_WIDTH,self.EXECUTION_SPEED))
        self.instructions.append(Instruction(2000,500,self.INSTRUCTION_WIDTH,self.EXECUTION_SPEED))
        self.instructions.append(Instruction(2000,600,self.INSTRUCTION_WIDTH,self.EXECUTION_SPEED))

    def update(self, tick):
        """Update logic for the instruction."""

        if self.state == self.State.MOVE1:
            if self.move1_action():
                self.state = self.State.EXECUTE1
        elif self.state == self.State.EXECUTE1:
            if self.execute1_action():
                self.state = self.State.JIGGLE
        elif self.state == self.State.JIGGLE:
            if self.jiggle_action():
                self.state = self.State.MOVE2
        elif self.state == self.State.MOVE2:
            if self.move2_action():
                self.state = self.State.EXECUTE2
        elif self.state == self.State.EXECUTE2:
            if self.execute2_action():
                self.state = self.State.FINISHED

        for instruction in self.instructions:
            instruction.update(tick)
    

    def draw(self, screen):
        """Draw the instruction on the screen."""
        for instruction in self.instructions:
            instruction.draw(screen) 

    def move1_action(self):
        """
        Move the instructions one by one to their respective positions, forming a line.

        Returns:
            bool: True if all instructions have completed their animations, False otherwise.
        """
        # Initialize the animation tracking attribute if not already set
        if not hasattr(self, "_instructions_moved"):
            self._instructions_moved = 0

        MOVE_SPEED = 30
        # Process the animation of each instruction sequentially
        if self._instructions_moved < self.NUM_INSTRUCTIONS:
            current_instruction = self.instructions[self._instructions_moved]

            if current_instruction.go_to( MOVE_SPEED,MOVE_SPEED,finalX=200 + 250 * self._instructions_moved, finalY=200):
                self._instructions_moved += 1
            #if current_instruction.go_to_smooth( finalX=200 + 250 * self._instructions_moved, finalY=200, MOVE_SPEED):
             #   self._instructions_moved += 1
        else:
            # All instructions have been moved, cleanup
            del self._instructions_moved
            return True

        # Animation is still in progress
        return False   
    
    def execute1_action(self):
        """
        Execute instructions 1 by 1.

        Returns:
            bool: True if all instructions have completed their animations, False otherwise.
        """
        # Initialize the animation tracking attribute if not already set
        if not hasattr(self, "_instructions_executed"):
            self._instructions_executed = 0

        if self.instructions[self._instructions_executed].is_executed():
            self._instructions_executed +=1
        else:
            self.instructions[self._instructions_executed].start_execution()
        
        if self._instructions_executed >= self.NUM_INSTRUCTIONS:
            del self._instructions_executed
            return True

        return False
    
    def jiggle_action(self):
        """
        Move all instructions up and down 10 times to make a jiggle effect, then reset their state.

        Returns:
            bool: True if all instructions have completed their animations, False otherwise.
        """
        for instruction in self.instructions:
            instruction.reset()

        return True
    
        # Initialize jiggle state if not already done
        if not hasattr(self, "_jiggle_times"):
            self._jiggle_times = 0  # Number of completed jiggle cycles
            self._jiggle_dir = 1   # Direction: 1 for up, -1 for down
        
        # Jiggle logic
        if self._jiggle_times < 10:
            for instruction in self.instructions:
                # Move instructions in the current jiggle direction
                instruction.move(deltaX=0, deltaY=5 * self._jiggle_dir)
            
            # Toggle direction after each movement
            self._jiggle_dir *= -1
            self._jiggle_times += 0.5  # Each up and down counts as one cycle
        else:
            # Reset instructions and cleanup state
            for instruction in self.instructions:
                instruction.reset()
            del self._jiggle_times
            del self._jiggle_dir
            return True
    
        return False

    
    def move2_action(self):
        """
        Move the instructions one by one to their respective positions, forming an stairs.

        Returns:
            bool: True if all instructions have completed their animations, False otherwise.
        """
        # Initialize the animation tracking attribute if not already set
        if not hasattr(self, "_instructions_moved"):
            self._instructions_moved = 0

        step_width = self.instructions[0].get_step_width()
        MOVE_SPEED = 30
        # Process the animation of each instruction sequentially
        if self._instructions_moved < self.NUM_INSTRUCTIONS:
            current_instruction = self.instructions[self._instructions_moved]

            if current_instruction.go_to( MOVE_SPEED,MOVE_SPEED,finalX=200 + step_width * self._instructions_moved, finalY=200 + (step_width+10) * self._instructions_moved):
                self._instructions_moved += 1
            #if current_instruction.go_to_smooth( finalX=200 + 250 * self._instructions_moved, finalY=200, MOVE_SPEED):
             #   self._instructions_moved += 1
        else:
            # All instructions have been moved, cleanup
            del self._instructions_moved
            return True

        # Animation is still in progress
        return False  
    
    def execute2_action(self):
        """
        Execute instructions in a stair-step pattern: the next instruction starts
        when the previous has executed 1 step.

        Returns:
            bool: True if all instructions have completed their animations, False otherwise.
        """
        # Initialize the animation tracking attribute if not already set
        if not hasattr(self, "_instructions_launched"):
            self._instructions_launched = 0

        if self._instructions_launched < len(self.instructions):
            # Get the current instruction
            current_instruction = self.instructions[self._instructions_launched]

            # If the current instruction has executed one step, move to the next
            if current_instruction.get_step_executing() >= 1:
                self._instructions_launched += 1
            else:
                # Start or continue executing the current instruction
                current_instruction.start_execution()

        # Check if all instructions have been executed
        num_instructions_finished = 0
        for instruction in self.instructions:
            if  instruction.is_executed():
                num_instructions_finished += 1

        if num_instructions_finished >= len(self.instructions):
            del self._instructions_launched
            return True

        return False
    
    def finish(self):
        """Return True if the scene is finished."""
        return self.state == self.State.FINISHED   