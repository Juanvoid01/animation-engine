import pygame
from objects.object import Object
import re
from utils.colors import *

class CodeString(Object):
    """Represents a piece of code visually in Pygame."""

    HIGHLIGHT_COLOR = (0, 100, 255, 100)
    LINE_NUMBER_COLOR = (150, 150, 150)
    MARGIN_BETWEEN_LINES = 5

    def __init__(self, posX, posY, width, font_path="fonts/consola.ttf", font_size=20, code_text=""):
        """
        Initialize the Code object.

        Args:
            posX (int): The x-coordinate of the top-left corner.
            posY (int): The y-coordinate of the top-left corner.
            width (int): The width of the code area.
            font_path (str): Path to the font file.
            font_size (int): Size of the font.
            code_text (str): Multiline string containing the code to render.
        """
        super().__init__(posX, posY, width, 100)
        self.font = pygame.font.Font(font_path, font_size)
        self.line_height = font_size + 4  # Add spacing between lines
        self.code_text = code_text
        self.highlighted_line = None
        self.LINE_NUMBER_WIDTH = self.font.size("000")[0] + 10  # Adjust based on digits

        # Syntax colors
        self.syntax_colors = {
            "keyword": COLOR_C_CODE_BLUE,
            "string": COLOR_C_CODE_LIGHT_BROWN,
            "literals": COLOR_C_CODE_LIGHT_GREEN,
            "comment": COLOR_C_CODE_DARK_GREEN,
            "include_library" : COLOR_C_CODE_LIGHT_BROWN,
            "action_keywords": COLOR_C_CODE_PURPLE,
            "bracket": COLOR_GOLD,
            "square_bracket": COLOR_GOLD,
            "parenthesis": COLOR_GOLD,
            "default_types": COLOR_C_CODE_BLUE,
            "custom_types": COLOR_C_CODE_GREEN,
            "function": COLOR_C_CODE_LIGHT_YELLOW,
            "variable_names": COLOR_C_CODE_LIGHT_BLUE,
            "default": COLOR_WHITE,
        }



        # Keywords and patterns for C/C++
        self.language_patterns = {
            "keyword": r"(class|struct|typedef|enum|namespace|public\:|private\:|protected\:|constexpr|const|static|virtual|override|true|false)",
            "string": r"\".*?\"|'.*?'",  # Matches quoted strings
            "literals": r"\b\d+(\.\d+)?\b",
            "comment": r"//.*|/\*.*?\*/",  # Matches single-line and multi-line comments
            "include_library": r"<.*?>|\".*?\"", 
            "action_keywords": r"(\#include|using|new|delete|while|for|if|else|switch|case|break|continue|return|default|goto)",
            "bracket": r"[\{\}]",
            "square_bracket": r"[\[\]]",
            "parenthesis": r"[\(\)]", 
            "default_types": r"\b(int|float|double|char|void|bool|short|long|unsigned|signed|size_t|auto)\b",
            "custom_types": r"\b(std|pepe|uint16_t)\b",
            "function": r"\b(asadad|main)\b",
            "variable_names": r"\b(i|pepes|a|asd)\b",
        }

    def update(self, tick):
        """Update logic for the code (e.g., animations if needed)."""
        pass

    def draw_highlighted_line(self, screen, line, lineX, lineY):
        line_width = len(line) * self.font.size(line[0])[0]
        highlight_surface = pygame.Surface((line_width, self.line_height))
        highlight_surface.set_alpha(self.HIGHLIGHT_COLOR[3])  # Set transparency
        highlight_surface.fill(self.HIGHLIGHT_COLOR[:3])  # Fill with RGB color
        screen.blit(highlight_surface, (lineX, lineY))

    def draw(self, screen):
        """Draw the code block on the screen with syntax highlighting and line selection."""
        lines = self.code_text.split("\n")
        y_offset = self.posY
        
        for index, line in enumerate(lines):

            # Draw line number
            line_number_text = self.font.render(str(index), True, (self.LINE_NUMBER_COLOR if self.highlighted_line != index else COLOR_WHITE) )
            screen.blit(line_number_text, (self.posX - self.LINE_NUMBER_WIDTH, y_offset))

            x_offset = self.posX

            if self.highlighted_line == index:
                self.draw_highlighted_line(screen=screen, line=line, lineX=self.posX, lineY=y_offset)

            tokens = self.tokenize_line(line)
            for token, color in tokens:
                rendered_text = self.font.render(token, True, color)
                screen.blit(rendered_text, (x_offset, y_offset))
                x_offset += rendered_text.get_width()
            
            y_offset += self.line_height + self.MARGIN_BETWEEN_LINES

    def tokenize_line(self, line):

        """Tokenize a single line of code into (token, color) pairs."""
        tokens = []
        pos = 0

        while pos < len(line):
            match = None
            color = self.syntax_colors["default"]

            # Preserve whitespace (spaces and tabs)
            if line[pos].isspace():
                space_match = re.match(r"\s+", line[pos:])
                if space_match:
                    tokens.append((space_match.group(0), self.syntax_colors["default"]))
                    pos += len(space_match.group(0))
                continue

            # Try matching all patterns
            for category, pattern in self.language_patterns.items():
                match = re.match(pattern, line[pos:])
                if match:
                    color = self.syntax_colors.get(category, self.syntax_colors["default"])
                    tokens.append((match.group(0), color))
                    pos += len(match.group(0))
                    break  # Stop at first match

            # If no match, treat it as a variable name (fallback)
            if not match:
                # Fallback for unmatched characters (e.g., operators, punctuation)
                tokens.append((line[pos], self.syntax_colors["default"]))
                pos += 1

        return tokens

    def change_code(self, new_code_text):
        """Update the displayed code dynamically."""
        self.code_text = new_code_text

    def highlight_line(self, line_index):
        """Set the selected line index for highlighting."""
        self.highlighted_line = line_index