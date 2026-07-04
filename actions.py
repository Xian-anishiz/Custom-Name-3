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

class ActionWithDirection(Action):
    def __init__(self, g_dx: int, g_dy: int) -> None:
        super().__init__()

        self.g_dx = g_dx
        self.g_dy = g_dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError

class MovementAction(ActionWithDirection):
    """Actions indicating intent to move"""

    def perform(self, engine: Engine, entity: Entity) -> None:
        g_dest_x = entity.grid_x + self.g_dx
        g_dest_y = entity.grid_y + self.g_dy

        if not engine.game_map.in_bounds(g_dest_x, g_dest_y):
            return # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][g_dest_x, g_dest_y]:
            return # Destination is blocked by a tile
        if engine.game_map.get_blocking_entity_at_location(entity, g_dest_x, g_dest_y):
            return # Destination is blocked by an entity
    
        entity.move(self.g_dx, self.g_dy)

class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        g_dest_x = entity.grid_x + self.g_dx
        g_dest_y = entity.grid_y + self.g_dy
        target = engine.game_map.get_blocking_entity_at_location(entity, g_dest_x, g_dest_y)
        if not target:
            return # No entity to attack
        
        print(f"You kick the {target.name}, much to iys annoyance!")

class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        g_dest_x = entity.grid_x + self.g_dx
        g_dest_y = entity.grid_y + self.g_dy

        if engine.game_map.get_blocking_entity_at_location(entity, g_dest_x, g_dest_y):
            return MeleeAction(self.g_dx, self.g_dy).perform(engine, entity)
        
        else:
            return MovementAction(self.g_dx, self.g_dy).perform(engine, entity)