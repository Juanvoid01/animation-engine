#scene.py

from objects.object import Object

class Scene(Object):
    """Scene"""

    def __init__(self):
        super().__init__(0, 0, 0, 0)

    def update(self, tick):
        pass
    
    def draw(self, screen):
        pass

    def finish(self):
       """Return True if the scene is finished."""
       pass 