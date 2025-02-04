#object.py

from abc import ABC, abstractmethod
import math

class Object(ABC):
    """Abstract base class for all objects in the game."""

    def __init__(self, posX=0, posY=0, sizeX=1, sizeY=1):
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY

    @abstractmethod
    def update(self, tick):
        """Update the object's state."""
        pass

    @abstractmethod
    def draw(self, screen):
        """Draw the object on the screen."""
        pass

    def set_pos(self, posX, posY):
        """Set the position of the object."""
        self.posX = posX
        self.posY = posY

    def set_size(self, sizeX, sizeY):
        """Set the size of the object."""
        self.sizeX = sizeX
        self.sizeY = sizeY

    def move(self, deltaX, deltaY):
        """Move the object by deltaX and deltaY."""
        self.posX += deltaX
        self.posY += deltaY

    def scale(self, factorX, factorY):
        """Scale the object by a factor."""
        self.sizeX *= factorX
        self.sizeY *= factorY

    def change_size(self, delta_size, target_width, target_height, maintain_center=False):
        """
        Adjust the size incrementally toward the target width and height.
        Stops adjusting when the size reaches the target size.

        Args:
            delta_size (float): The absolute change in size per call.
            target_width (float): The target width to stop at.
            target_height (float): The target height to stop at.
            maintain_center (bool): Whether to adjust the position to keep the square centered.

        Returns:
            bool: True if the object has reached the target size, False otherwise.
        """
        # Ensure delta_size is positive
        delta_size = abs(delta_size)

        if maintain_center:
            # Calculate half the change in size for width and height
            shift_x = delta_size / 2 if self.sizeX != target_width else 0
            shift_y = delta_size / 2 if self.sizeY != target_height else 0

            # Adjust the position incrementally to keep the square centered
            if self.sizeX < target_width:
                self.posX -= shift_x
            elif self.sizeX > target_width:
                self.posX += shift_x

            if self.sizeY < target_height:
                self.posY -= shift_y
            elif self.sizeY > target_height:
                self.posY += shift_y

        # Adjust width and height incrementally
        if self.sizeX < target_width:
            self.sizeX = min(self.sizeX + delta_size, target_width)
        elif self.sizeX > target_width:
            self.sizeX = max(self.sizeX - delta_size, target_width)

        if self.sizeY < target_height:
            self.sizeY = min(self.sizeY + delta_size, target_height)
        elif self.sizeY > target_height:
            self.sizeY = max(self.sizeY - delta_size, target_height)

        # Check if the target size has been reached
        return self.sizeX == target_width and self.sizeY == target_height



    def go_to(self, deltaX, deltaY, finalX, finalY):

        """
        Move the object incrementally by deltaX and deltaY towards a final position.
        Stops moving once the object reaches or exceeds the target coordinates.

        Args:
            deltaX (float): The absolute change in x-coordinate per call.
            deltaY (float): The absolute change in y-coordinate per call.
            finalX (float): The target x-coordinate to stop at.
            finalY (float): The target y-coordinate to stop at.

        Returns:
            bool: True if the object has reached the target position, False otherwise.
        """
        # Ensure deltaX and deltaY are positive
        deltaX = deltaX + abs(finalX-self.posX)/64
        deltaY = deltaY + abs(finalY-self.posY)/64

        # Update X position
        if self.posX < finalX:
            self.posX = min(self.posX + deltaX, finalX)
        elif self.posX > finalX:
            self.posX = max(self.posX - deltaX, finalX)

        # Update Y position
        if self.posY < finalY:
            self.posY = min(self.posY + deltaY, finalY)
        elif self.posY > finalY:
            self.posY = max(self.posY - deltaY, finalY)

        # Check if both X and Y have reached their targets
        return self.posX == finalX and self.posY == finalY
    
    def go_to_smooth(self, finalX, finalY, speed=5):
        """
        Move the object incrementally towards a final position with an ease-in-out effect.
        The movement accelerates at the start and decelerates as it approaches the final position.

        Args:
            finalX (float): The target x-coordinate to stop at.
            finalY (float): The target y-coordinate to stop at.
            speed (float): The base speed factor controlling movement.

        Returns:
            bool: True if the object has reached the target position, False otherwise.
        """

        if not hasattr(self, "startX"):
            self.startX = self.posX
        if not hasattr(self, "startY"):
            self.startY = self.posY

        # Calculate total distances
        total_distanceX = abs(finalX - self.startX)
        total_distanceY = abs(finalY - self.startY)

        # Calculate remaining distances
        distanceX = abs(finalX - self.posX)
        distanceY = abs(finalY - self.posY)

        # Progress (0 to 1), ensuring no division by zero
        progressX = 1 - (distanceX / total_distanceX) if total_distanceX != 0 else 1
        progressY = 1 - (distanceY / total_distanceY) if total_distanceY != 0 else 1

        # Easing function: cubic ease-in-out
        def cubic_ease_in_out(t):
            return 3 * t**2 - 2 * t**3  # Smooth acceleration and deceleration

        easingX = cubic_ease_in_out(progressX)
        easingY = cubic_ease_in_out(progressY)

        # Dynamically adjust movement speed
        stepX = (finalX - self.posX) * easingX * speed / (distanceX + 1e-5)
        stepY = (finalY - self.posY) * easingY * speed / (distanceY + 1e-5)

        # Update position
        self.posX += stepX
        self.posY += stepY

        # Check if we are close enough to stop
        at_target = abs(self.posX - finalX) < 0.1 and abs(self.posY - finalY) < 0.1

        if at_target:
            self.posX = finalX
            self.posY = finalY
            del self.startX
            del self.startY
            return True

        return False