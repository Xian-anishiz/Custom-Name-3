from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    """Base class for all game actions"""
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to determine its scope.

       `engine` is the scope this action is being performed in.

       `entity` is the object performing the action.

       This method must be overridden by Action subclasses.
       """
        raise NotImplementedError

class EscapeAction(Action):
    """Actions that exits the game or menu"""
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class MovementAction(Action):
    """Actions indicating intent to move"""
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.grid_x + self.dx
        dest_y = entity.grid_y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination is blocked by a tile
        
    
        entity.move(self.dx, self.dy)