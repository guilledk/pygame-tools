#!/usr/bin/env python3

import math

from typing import Optional

import pygame

from pygame import Surface
from pygame.math import Vector2
from pygame_tools.ecs import Component


class Transform(Component):

    def __init__(self):
        self.pos = Vector2()


class Physics(Component):

    def __init__(self):
        self.vel = Vector2()
        self.max_vel = Vector2()
        self.friction = 0.4

    def start(self):
        self.transform = self.entity.require_component(Transform)[0]

    def update(self, dt: float):
        if self.friction > 0:
            vlen = self.vel.length()
            if vlen > 0.5:
                self.vel.scale_to_length(vlen * (1.0 - (self.friction * dt)))
            else:
                self.vel.x = self.vel.y = 0

        if self.max_vel.x != 0:
            self.vel.x = min(self.max_vel.x, self.vel.x)

        if self.max_vel.y != 0:
            self.vel.y = min(self.max_vel.y, self.vel.y)

        # move
        self.transform.pos += self.vel * dt

    def accelerate(self, angle: int, value: int):
        self.vel += Vector2().from_polar((value, math.radians(angle)))

    def accelerate(self, vector: Vector2):
        self.vel += vector

class Renderer(Component):

    def __init__(self):
        self.target: Optional[Surface] = None
        self.texture: Optional[Surface] = None

    def start(self):
        self.transform = self.entity.require_component(Transform)[0]

    def draw(self):
        assert self.target is not None
        assert self.texture is not None
        self.target.blit(
            self.texture,
            (self.transform.pos.x, self.transform.pos.y)
        )