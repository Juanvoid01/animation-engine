#scene_code.py

from scene.scene import Scene
from objects.code_string import CodeString
from enum import Enum, auto

SAMPLE_CODE_1 = """
int calculate_max (int a, int b) {

    int max_number;

    if (a > b) {
        max_number = a;
    } else if (a <= b){
        max_number = b;
    }

    return max_number;
}
"""

class SceneCode(Scene):
    """Scene"""


    class State(Enum):
        INITIALIZE = auto()
        SELECT_A = auto()
        TYPE_A = auto()
        SELECT_A_CONDITION = auto()
        TYPE_A_CONDITION = auto()
        SELECT_B = auto()
        TYPE_B = auto()
        SELECT_B_CONDITION = auto()
        TYPE_B_CONDITION = auto()
        ERASE_ANCIENT = auto()
        FINISHED = auto()

    def __init__(self):
        super().__init__()
        sample_code = SAMPLE_CODE_1
        self.code = CodeString(100, 50, 700, code_text=sample_code, custom_types=[], variables=["a", "b", "max_number"], functions=["calculate_max"])
        self.code.highlight_line(24)

        self.state = self.State.INITIALIZE

    def update(self, tick):

        if tick % 6 != 0: # every three ticks
            return
        
        if  self.state == self.State.INITIALIZE: 
            self.state = self.State.SELECT_A
        elif self.state == self.State.SELECT_A:
            self.code.highlight_line(6)
            self.state = self.State.TYPE_A
        elif self.state == self.State.TYPE_A:
            if self.code.type_and_erase_text(line_index=3,num_characters_to_erase=1,text=" = a"): 
                self.state = self.State.SELECT_A_CONDITION
        elif self.state == self.State.SELECT_A_CONDITION:
            self.code.highlight_line(5)
            self.state = self.State.TYPE_A_CONDITION
        elif self.state == self.State.TYPE_A_CONDITION:
            if self.code.type_and_erase_text(line_index=3,num_characters_to_erase=0,text=" * (a > b)"):
                self.state = self.State.SELECT_B

        elif self.state == self.State.SELECT_B:
            self.code.highlight_line(8)
            self.state = self.State.TYPE_B
        elif self.state == self.State.TYPE_B:
            if self.code.type_and_erase_text(line_index=3,num_characters_to_erase=0,text=" + b"): 
                self.state = self.State.SELECT_B_CONDITION
        elif self.state == self.State.SELECT_B_CONDITION:
            self.code.highlight_line(7)
            self.state = self.State.TYPE_B_CONDITION
        elif self.state == self.State.TYPE_B_CONDITION:
            if self.code.type_and_erase_text(line_index=3,num_characters_to_erase=0,text=" * (a <= b);"):
                self.code.highlight_line(None)  
                self.state = self.State.ERASE_ANCIENT
        elif self.state == self.State.ERASE_ANCIENT:

            erase_results = [
                self.code.erase_text(line_index=5, num_characters_to_erase=self.code.get_line_lenght(5)),
                self.code.erase_text(line_index=6, num_characters_to_erase=self.code.get_line_lenght(6)),
                self.code.erase_text(line_index=7, num_characters_to_erase=self.code.get_line_lenght(7)),
                self.code.erase_text(line_index=8, num_characters_to_erase=self.code.get_line_lenght(8)),
                self.code.erase_text(line_index=9, num_characters_to_erase=self.code.get_line_lenght(9)),
            ]
            
            if all(erase_results):
                for i in range(9, 3, -1):  # Removes lines from 9 down to 5
                    self.code.remove_line(i)

                self.state = self.State.FINISHED

        self.code.update(tick)
    
    def draw(self, screen):
        self.code.draw(screen)

    def finish(self):
       return False

       return self.state == self.State.FINISHED
