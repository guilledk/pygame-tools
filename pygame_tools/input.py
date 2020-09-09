#!/usr/bin/env python3

import pygame


class Keyboard:

	def __init__(self):

		self._prev_frame_keys = pygame.key.get_pressed()
		self._frame_keys = self._prev_frame_keys