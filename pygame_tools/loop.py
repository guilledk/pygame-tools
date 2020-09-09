#!/usr/bin/env python3

from typing import Tuple, Optional, Callable

import pygame

from pygame.time import Clock
from pygame.locals import QUIT
from pygame_tools.input import Keyboard


class Gameloop:

    def __init__(
        self,
        display_size: Tuple[int, int],
        display_caption: str
    ):
        self.call_update: Optional[Callable[[float], None]] = None
        self.call_draw: Optional[Callable[[None], None]] = None
        self.level: Optional['Level'] = None
        self.keyboard: Optional[Keyboard] = None

        pygame.init()
        self.display = pygame.display.set_mode(display_size)
        self.clock = Clock()
        pygame.display.set_caption(display_caption)

    def run(self):
        self.keyboard = Keyboard()
        while True:
            pygame.event.pump()
            self.keyboard.update()
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
        # hook callbacks
        self.call_update = level.update
        self.call_draw = level.draw

        # update static references
        level.game = self
        self.level = level

        # update static references for all components
        for ename, entity in level.entities.items():
            for comp in entity.components:
                comp.level = self.level
                comp.game = self

        # one time callback
        level.start()