import pygame
from actions import Action, EscapeAction, MovementAction

class EventHandler:
    def get_actions(self, player_can_move: bool) -> list[Action]:
        actions: list[Action] = []

        # discrete
        discrete_events = self.handle_events()
        actions.extend(discrete_events)

        # continuous
        if player_can_move:
            continuous_events = self.handle_continuous_input()
            actions.extend(continuous_events)

        return actions
        
    def handle_events(self) -> list[Action]:
        """Collects all pygame events and dispatches them returning a list of Actions"""
        actions: list[Action] = []

        for event in pygame.event.get():
            action = self.dispatch(event)
            if action:
                actions.append(action)

        return actions
    
    def handle_continuous_input(self) -> list[MovementAction]:
        actions: list[MovementAction] = []
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            actions.append(MovementAction(0, -1))
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            actions.append(MovementAction(0, 1))
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            actions.append(MovementAction(-1, 0))
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            actions.append(MovementAction(1, 0))

        return actions
    
    def dispatch(self, event: pygame.event.Event) -> Action | None:
        """Routes a single Pygame event to its corresponding helper method."""
        if event.type == pygame.QUIT:
            return self.ev_quit()
        elif event.type == pygame.KEYDOWN:
            return self.ev_keydown(event)
        
        return None

    def ev_quit(self) -> Action | None:
        """Handles windows closing"""
        raise SystemExit()
    
    def ev_keydown(self, event: pygame.event.Event) -> Action | None:
        key = event.key
        if key == pygame.K_ESCAPE:
            return EscapeAction()
        
        return None
    