from entity import Player, Troll, Orc
from constants import *

player = Player(
    grid_x=GRID_WIDTH // 2, 
    grid_y=GRID_HEIGHT // 2, 
    radius=TILE_SIZE // 2,
    name="Player",
    block_movement=True,
)

orc = Orc(
    grid_x=GRID_WIDTH // 2, 
    grid_y=GRID_HEIGHT // 2, 
    radius=TILE_SIZE // 2,
    name="Orc",
    block_movement=True,
)

troll = Troll(
    grid_x=GRID_WIDTH // 2, 
    grid_y=GRID_HEIGHT // 2, 
    radius=TILE_SIZE,
    name="Troll",
    block_movement=True,
)
