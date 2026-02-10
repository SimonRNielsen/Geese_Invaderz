from abc import ABC, abstractmethod
from GameObject import GameObject
from Components import SpriteRenderer, Animator, Collider
from Enums import Entity
import random, pygame

class Builder(ABC):

    @classmethod
    @abstractmethod
    def build(self):
        pass

    def get_gameObject(self) -> GameObject:
        pass

class PlayerBuilder(Builder):

    def build(self, position):
        self._gameObject = GameObject(position)
        self._gameObject.add_component(SpriteRenderer(Entity.PLAYER))
        animator = self._gameObject.add_component(Animator())
        animator.play_animation(Entity.PLAYER)
        self._gameObject.add_component(Collider())
    
    def get_gameObject(self) -> GameObject:
        return self._gameObject