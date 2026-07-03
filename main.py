import pygame, sys, copy
import entity_factories
from input_handlers import EventHandler
from output_handler import OutputHandler
from engine import Engine
from constants import *
from procgen import generate_dungeon


def main() -> None:
    #* set-up
    pygame.init()
    pygame.display.set_caption('Custom Name 3')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #* Entity details
    player = copy.deepcopy(entity_factories.player)

    #* handlers
    event_handler = EventHandler()
    output_handler = OutputHandler()
    game_map = generate_dungeon(MAX_ROOMS,
                                ROOM_MIN_SIZE,
                                ROOM_MAX_SIZE,
                                MAP_WIDTH, 
                                MAP_HEIGHT,
                                player,
                                MAX_MONSTERS_PER_ROOM)
    engine = Engine(event_handler, output_handler, game_map, player, screen)

    engine.start()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()