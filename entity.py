from __future__ import annotations

import copy
import pygame
from constants import TILE_SIZE
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, 
                 grid_x: int, 
                 grid_y: int, 
                 color: str, 
                 name: str = "<Unnamed>",
                 block_movement: bool = False,
                 speed: int = 0,) -> None:
        self._color = color
        self._name = name
        self._block_movement = block_movement
        
        # Logical grid position
        self._grid_x = grid_x
        self._grid_y = grid_y

        # Visual position on screen
        self._pixel_x = grid_x * TILE_SIZE
        self._pixel_y = grid_y * TILE_SIZE

        # Target position
        self._target_pixel_x = self._pixel_x
        self._target_pixel_y = self._pixel_y

        self._is_moving = False
        
        # Every entity has a speed. Default is 0 (static entities like items or traps)
        self._speed = speed

    # TODO replace this with a Factory instead of deepcopy
    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """spawnh a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.grid_x = x
        clone.grid_y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int):
        # Prevent starting a new move if we are already moving
        if self._is_moving:
            return
            
        self._grid_x += dx
        self._grid_y += dy

        self._target_pixel_x = self._grid_x * TILE_SIZE
        self._target_pixel_y = self._grid_y * TILE_SIZE
        self._is_moving = True

    def update(self, dt: float):
        if not self._is_moving:
            return
        
        step = self._speed * dt # how far to move this specific frame

        # move horizontally towards target
        if self._pixel_x < self._target_pixel_x:
            self._pixel_x = min(self._pixel_x + step, self._target_pixel_x)
        elif self._pixel_x > self._target_pixel_x:
            self._pixel_x = max(self._pixel_x - step, self._target_pixel_x)

        # move vertically towards target
        if self._pixel_y < self._target_pixel_y:
            self._pixel_y = min(self._pixel_y + step, self._target_pixel_y)
        elif self._pixel_y > self._target_pixel_y:
            self._pixel_y = max(self._pixel_y - step, self._target_pixel_y)

        # reached target
        if self._pixel_x == self._target_pixel_x and self._pixel_y == self._target_pixel_y:
            self._is_moving = False

    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError
    
    @property
    def center(self) -> tuple[int, int]:
        raise NotImplementedError

    @property
    def is_moving(self) -> bool:
        return self._is_moving
    
    @property
    def pos(self) -> tuple[int, int]:
        return (int(self._pixel_x), int(self._pixel_y))
    
    @property
    def color(self):
        return self._color
    
    @property
    def grid_x(self) -> int:
        return self._grid_x
    
    @grid_x.setter
    def grid_x(self, x: int) -> None:
        self._grid_x = x
        self._pixel_x = x * TILE_SIZE
        self._target_pixel_x = self._pixel_x

    @property
    def grid_y(self) -> int:
        return self._grid_y
    
    @grid_y.setter
    def grid_y(self, y: int) -> None:
        self._grid_y = y
        self._pixel_y = y * TILE_SIZE
        self._target_pixel_y = self._pixel_y

# =====================================================================
# SUBCLASSES
# =====================================================================
# ! right now this assumes all entities are circle
# TODO readjust to make it applicable for other shapes

class Player(Entity):
    def __init__(self, grid_x: int, 
                 grid_y: int, 
                 radius: int, 
                 name: str, 
                 block_movement: bool) -> None:
        # We call the super class's __init__ first! 
        # We explicitly pass up the Player's specific color and speed (150).
        super().__init__(
            grid_x=grid_x, 
            grid_y=grid_y, 
            color="yellow", 
            speed=150,
            name=name,
            block_movement=block_movement
        )
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    @property
    def center(self) -> tuple[int, int]:
        x = self._pixel_x + TILE_SIZE // 2
        y = self._pixel_y + TILE_SIZE // 2
        return (int(x), int(y))

class NPC(Entity):
    def __init__(self, grid_x: int, 
                 grid_y: int, 
                 radius: int, 
                 name: str, 
                 block_movement: bool) -> None:
        super().__init__(
            grid_x=grid_x, 
            grid_y=grid_y, 
            color="green",
            name=name,
            block_movement=block_movement
        )
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    @property
    def center(self) -> tuple[int, int]:
        x = self._pixel_x + TILE_SIZE // 2
        y = self._pixel_y + TILE_SIZE // 2
        return (int(x), int(y))

class Troll(Entity):
    def __init__(self, grid_x: int, 
                 grid_y: int, 
                 radius: int, 
                 name: str, 
                 block_movement: bool) -> None:
        super().__init__(
            grid_x=grid_x, 
            grid_y=grid_y, 
            color="red",
            name=name,
            block_movement=block_movement
        )
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    @property
    def center(self) -> tuple[int, int]:
        x = self._pixel_x + TILE_SIZE // 2
        y = self._pixel_y + TILE_SIZE // 2
        return (int(x), int(y))

class Orc(Entity):
    def __init__(self, grid_x: int, 
                 grid_y: int, 
                 radius: int, 
                 name: str, 
                 block_movement: bool) -> None:
        super().__init__(
            grid_x=grid_x, 
            grid_y=grid_y, 
            color="orange",
            name=name,
            block_movement=block_movement
        )
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    @property
    def center(self) -> tuple[int, int]:
        x = self._pixel_x + TILE_SIZE // 2
        y = self._pixel_y + TILE_SIZE // 2
        return (int(x), int(y))