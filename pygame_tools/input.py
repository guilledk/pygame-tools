#!/usr/bin/env python3

import pygame


class Keyboard:

	def __init__(self):
		self._prev_frame_keys = pygame.key.get_pressed()
		self._frame_keys = self._prev_frame_keys

	def update(self):
		self._prev_frame_keys = self._frame_keys
		self._frame_keys = pygame.key.get_pressed()

	def was_pressed(self, key):
		return self._frame_keys[key] and not self._prev_frame_keys[key]

	def was_released(self, key):
		return not self._frame_keys[key] and self._prev_frame_keys[key]

	def is_down(self, key):
		return self._frame_keys[key]