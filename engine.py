import tcod
from entity import Player
from input_handlers import EventHandler
from output_handler import OutputHandler
from game_map import GameMap
import pygame

class Engine:
    def __init__(self,
                 event_handler: EventHandler, 
                 output_handler: OutputHandler, 
                 game_map: GameMap,
                 player: Player,
                 screen: pygame.Surface) -> None:
        self._event_handler = event_handler
        self._output_handler = output_handler
        self._game_map = game_map
        self._player = player

        self._running = True
        self._clock = pygame.time.Clock()
        self._dt = 0
        self._screen = screen
        self.update_fov()

    def handle_events(self) -> None:
        actions = self._event_handler.get_actions(not self._player.is_moving)

        for action in actions:
            action.perform(self, self._player)

        self.update_fov() # Update the FOV before the players next action

    def update_fov(self) -> None:
        """Recompute the visible area based pon the players point of view"""
        self._game_map.visible[:] = tcod.map.compute_fov(
            self._game_map.tiles["transparent"],
            (self._player.grid_x, self._player.grid_y),
            radius = 8,
        )

        # If a tile is "visible" it should be added to "explored"
        self._game_map.explored |= self._game_map.visible

    def update(self) -> None:
        self._player.update(self._dt)

    def render(self) -> None:
        self._output_handler.clear_screen(self._screen)

        self._game_map.render(self._screen)

    def start(self) -> None:
        while self._running:
            #* --- PYGAME EVENT LOOP ---

            #* --- GAME LOGIC ---
            self.handle_events()
            if not self._running:
                return

            #* --- GAME UPDATE ---
            self.update()

            #* --- PYGAME RENDERING ---
            self.render()

            pygame.display.flip()
            self._dt = self._clock.tick(60) / 1000.0

    @property
    def game_map(self):
        return self._game_map