#!/usr/bin/env python3

from typing import Tuple, Optional, Callable

import pygame

from pygame.time import Clock
from pygame.locals import QUIT


class Gameloop:

    def __init__(
        self,
        display_size: Tuple[int, int],
        display_caption: str
    ):
        self.call_update: Optional[Callable[[float], None]] = None
        self.call_draw: Optional[Callable[[None], None]] = None

        pygame.init()
        self.display = pygame.display.set_mode(display_size)
        self.clock = Clock()
        pygame.display.set_caption(display_caption)

    def run(self):
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            self.display.fill((0,0,0))
            
            dtms = self.clock.tick()
            dt = dtms / 1000.0

            self.call_update(dt)
            self.call_draw()
            pygame.display.update()

    def set_level(self, level: 'Level'):
        self.call_update = level.update
        self.call_draw = level.draw
        level.game = self
        level.start()
