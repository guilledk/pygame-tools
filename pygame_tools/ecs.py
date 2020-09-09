#!/usr/bin/env python3

from abc import ABC, abstractmethod 
from typing import Optional, List, Dict

from .loop import Gameloop


class Component(ABC):

    def __init__(self, entity):
        self.entity = entity

    def start(self):
        ...

    def update(self, dt: float):
        ...

    def draw(self):
        ...


class Entity:

    def __init__(self, name: str, parent: Optional['Entity']):
        self.name = name
        self.parent = parent

        self.level: Optional[Level] = None
        self.childs: List['Entity'] = list()
        self.components: List[Component] = list()

    def require_component(self, comp_type) -> List[Component]:
        search = [
            comp for comp in self.components if isinstance(comp, comp_type)
        ]
        assert len(search) > 0
        return search

    def add_component(self, comp_type) -> Component:
        new_comp = comp_type(self)
        self.components.append(new_comp)
        return new_comp

    def start(self):
        for component in self.components:
            component.start()

    def update(self, dt: float):
        for component in self.components:
            component.update(dt)

    def draw(self):
        for component in self.components:
            component.draw()

class Level:

    def __init__(self, name: str):
        self.name = name

        self.game: Optional[Gameloop] = None
        self.entities: Dict[str, Entity] = dict()

    def spawn(self, ent: Entity):
        assert ent.name not in self.entities
        self.entities[ent.name] = ent
        ent.level = self

    def start(self):
        for ename, entity in self.entities.items():
            entity.start()

    def update(self, dt: float):
        for ename, entity in self.entities.items():
            entity.update(dt)

    def draw(self):
        for ename, entity in self.entities.items():
            entity.draw()