#!/usr/bin/env python3

import json
import pathlib

from collections.abc import MutableMapping

import pygame


class SpriteSheet(MutableMapping):

    VERSION = '1'

    def __init__(self, resource_path):
        self.resource_path = resource_path

        self._sheet = dict()
        self._sheet_width = 0
        self._sheet_height = 0
        self.tile_w = 0
        self.tile_h = 0

        self._res_path = pathlib.Path(self.resource_path)

        if self._res_path.is_dir():
            self.from_dir()
        elif self._res_path.suffix == '.json':
            self.from_manifest()

    def from_manifest(self):

        with open(self._res_path, 'r') as manifest_file:
            manifest = json.loads(manifest_file.read())

        assert "header" in manifest
        assert "tile_w" in manifest
        assert "tile_h" in manifest
        assert "sprites" in manifest
        assert "texture" in manifest

        self.tile_w = manifest['tile_w']
        self.tile_h = manifest['tile_h']

        texture = pygame.image.load(
            f"{self._res_path.parent}/{manifest['texture']}"
        )
        texture.convert_alpha()

        for y, sprite in enumerate(manifest['sprites']):
            self._sheet[sprite['name']] = []
            for x in range(sprite['frames']):
                tex_fragment = pygame.Surface((self.tile_w, self.tile_h), pygame.SRCALPHA)
                tex_fragment.blit(
                    texture,
                    (0,0),
                    area=pygame.Rect(
                        x * self.tile_w,
                        y * self.tile_h,
                        self.tile_w,
                        self.tile_h
                    )
                )
                self._sheet[sprite['name']].append(tex_fragment)

            self._sheet_width = max(self._sheet_width, len(self._sheet[sprite['name']]))
        self._sheet_height = len(self._sheet)


    def from_dir(self):
        for img_path in self._res_path.glob('*.png'):
            splt_stem = img_path.stem.split("_")

            sprite = splt_stem[0]
            if sprite not in self._sheet:
                self._sheet[sprite] = list()

            if len(splt_stem) == 2:
                index = int(splt_stem[1])
                while len(self._sheet[sprite]) < index + 1:
                    self._sheet[sprite].append(None)
                self._sheet[sprite][index] = pygame.image.load(str(img_path))
                self._sheet[sprite][index].convert_alpha()

                self._sheet_width = max(self._sheet_width, len(self._sheet[sprite]))

                img_rect = self._sheet[sprite][index].get_rect()

            else:
                self._sheet[sprite].append(
                    pygame.image.load(str(img_path))
                )
                img_rect = self._sheet[sprite][0].get_rect()
                self._sheet[sprite][0].convert_alpha()

            if self.tile_w != 0:
                assert self.tile_w == img_rect.w
            else:
                self.tile_w = img_rect.w

            if self.tile_h != 0:
                assert self.tile_h == img_rect.h
            else:
                self.tile_h = img_rect.h

        self._sheet_height = len(self._sheet)

    def export(self, output_path):

        out_path = pathlib.Path(output_path)

        manifest = dict()

        manifest['header'] = f"pygame_tools.sheet.SpriteSheet-v{SpriteSheet.VERSION}"
        manifest['tile_w'] = self.tile_w
        manifest['tile_h'] = self.tile_h
        manifest['sprites'] = []
        manifest['texture'] = out_path.name
        for sprite in self._sheet:
            manifest['sprites'].append(
                { 'name': sprite, 'frames': len(self._sheet[sprite]) }
            )

        with open(
            f"{out_path.parent}/manifest.json",
            "w+"
        ) as manifest_file:
            manifest_file.write(
                json.dumps(
                    manifest,
                    indent=4,
                    sort_keys=True
                )
            )

        texture = pygame.Surface(
            (
                self.tile_w * self._sheet_width,
                self.tile_h * self._sheet_height
            ),
            pygame.SRCALPHA
        )

        for y, sprite in enumerate(self._sheet):
            y_pos = y * self.tile_h
            for x, frame in enumerate(self._sheet[sprite]):
                x_pos = x * self.tile_w
                texture.blit(self._sheet[sprite][x], (x_pos, y_pos))

        pygame.image.save(texture, args.output_path)

    def __getitem__(self, key):
        return self._sheet[key]

    def __setitem__(self, key, value):
        self._sheet[key] = value

    def __delitem__(self, key):
        del self._sheet[key]

    def __iter__(self):
        return iter(self._sheet)

    def __len__(self):
        return self._sheet_width * self._sheet_height

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'resource_path',
        type=str
    )
    parser.add_argument(
        'output_path',
        type=str
    )
    args = parser.parse_args()

    pygame.init()
    display = pygame.display.set_mode((1, 1))
    SpriteSheet(args.resource_path).export(args.output_path)