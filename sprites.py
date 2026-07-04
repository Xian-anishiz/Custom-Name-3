from pygame import Surface, SRCALPHA
"""Stores the sprite placeholder details for later styling"""
# height, width, color

def create_placeholder_sprite(width_px: int, height_px: int, color: tuple[int, int, int]):
    surf = Surface((width_px, height_px), SRCALPHA)
    surf.fill(color)
    return surf

player_sprite = create_placeholder_sprite(16, 16, (255, 255, 0))
npc_sprite = create_placeholder_sprite(16, 16, (0, 255, 0))
orc_sprite = create_placeholder_sprite(16, 16, (255, 0, 255))
troll_sprite = create_placeholder_sprite(32, 32, (255, 0, 0))