#!/usr/bin/env python3

import math

from typing import Optional

from pygame import Surface
from pygame.math import Vector2

from pygame_tools.ecs import Component


class Transform(Component):

    def __init__(self, entity):
        super().__init__(entity)

        self.pos = Vector2()


class Physics(Component):

    def __init__(self, entity):
        super().__init__(entity)
        
        self.transform = entity.require_component(Transform)[0]
        self.vel = Vector2()
        self.friction = 20

    def update(self, dt: float):
    	# apply friction
    	vlen = self.vel.length()
    	if vlen > 0:
    		self.vel.scale_to_length(max(0, vlen - (self.friction * dt)))

    	# move
    	self.transform.pos += self.vel * dt

    def accelerate(self, angle: int, value: int):
    	self.vel += Vector2().from_polar((value, math.radians(angle)))


class Renderer(Component):

    def __init__(self, entity):
        super().__init__(entity)

        self.target: Optional[Surface] = None
        self.texture: Optional[Surface] = None
        self.transform = entity.require_component(Transform)[0]

    def draw(self):
    	assert self.target is not None
    	assert self.texture is not None
    	self.target.blit(
    		self.texture,
    		(self.transform.pos.x, self.transform.pos.y)
    	)