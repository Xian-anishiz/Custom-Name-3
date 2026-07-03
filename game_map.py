from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np #type:ignore
import pygame
import tile_types
from collections.abc import Iterable

if TYPE_CHECKING:
    from entity import Entity

class GameMap:
    def __init__(self, 
                 width: int, 
                 height: int,
                 tile_size: int,
                 entities: Iterable[Entity]) -> None:
        self._width, self._height = width, height
        self._tile_size = tile_size
        self._entities = set(entities)
        
        self._tiles = np.full((width, height), fill_value = tile_types.wall, order="F")

        self._visible = np.full((width, height), fill_value = False, order="F")
        self._explored = np.full((width, height), fill_value = False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self._width and 0 <= y < self._height
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array. then draw it with the "light" colors
        If it isn't, but it's in the "explored" array, then draw it with the "dark"
        Otherwise, the default is "SHROUD"
        """
        tile_graphic = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for x in range(self._width):
            for y in range(self._height):
                # Extract a single tile's RGB color and coerce numpy scalars to Python ints.
                bg = tile_graphic[x, y]["bg"]
                bg_color = (int(bg[0]), int(bg[1]), int(bg[2]))

                # 3. Calculate the pixel positions based on your tile-to-pixel ratio
                pixel_x = x * self._tile_size
                pixel_y = y * self._tile_size
                
                # 4. Draw the tile as a solid colored block matching the tutorial's style
                pygame.draw.rect(
                    screen,
                    bg_color,
                    pygame.Rect(pixel_x, pixel_y, self._tile_size, self._tile_size)
                )

        for entity in self._entities:
            # Only print entities that are in the FOV
            if self._visible[entity.grid_x, entity.grid_y]:
                entity.draw(screen)

    @property
    def tiles(self):
        return self._tiles
    
    @property
    def visible(self):
        return self._visible
    
    @property
    def explored(self):
        return self._explored

    @explored.setter
    def explored(self, value: np.ndarray) -> None:
        self._explored = np.asarray(value, dtype=bool) | self._visible

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def entities(self):
        return self._entities