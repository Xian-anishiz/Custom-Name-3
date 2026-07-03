import pygame

class OutputHandler:
    def clear_screen(self, screen: pygame.Surface) -> None:
        screen.fill("black")

    def draw_circle(self, screen: pygame.Surface,  color: str, pos: tuple[int, int], radius: int) -> None:
        pygame.draw.circle(screen, color, pos, radius)