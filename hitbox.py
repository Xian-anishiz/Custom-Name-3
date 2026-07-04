import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

class Hitbox:
    def __init__(self, entity: "Entity") -> None:
        """pixel x and y refers to the anchor points"""
        self._entity = entity
        self._hitbox = pygame.Rect(0, 0, entity.width, entity.height)
        self._update_hitbox_position()

    def _update_hitbox_position(self):
        """Keeps the hitbox glued to the center of the moving sprite"""
        s_center_x = self._entity.pixel_x + (self._entity.width / 2)
        s_center_y = self._entity.pixel_y + (self._entity.height / 2)

        self._hitbox.center = (s_center_x, s_center_y)

    def update(self):
        self._update_hitbox_position()
        
    def collides(self, other: "Hitbox") -> bool:
        return self.hitbox.colliderect(other.hitbox)
    
    @property
    def hitbox(self):
        return self._hitbox
    
    @property
    def left(self) -> int:
        return self.hitbox.left

    @property
    def right(self) -> int:
        return self.hitbox.right
    
    @property
    def top(self) -> int:
        return self.hitbox.top
    
    @property
    def bottom(self) -> int:
        return self.hitbox.bottom