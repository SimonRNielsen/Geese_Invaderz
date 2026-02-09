from abc import ABC, abstractmethod
from GameObject import GameObject
from Components import SpriteRenderer, Animator, Collider
import random, pygame

class Builder(ABC):

    @classmethod
    @abstractmethod
    def build(self):
        pass

    def get_gameObject(self) -> GameObject:
        pass