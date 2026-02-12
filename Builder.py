from abc import ABC, abstractmethod
from GameObject import GameObject
from Components import SpriteRenderer, Animator, Collider
from Enums import Entities
from Player import Player
import random, pygame

class Builder(ABC):

    @classmethod
    @abstractmethod
    def build(self):
        pass

    def get_gameObject(self) -> GameObject:
        pass

class PlayerBuilder(Builder):

    def build(self):
        #Startposition: venstre side midt på skærmen
        start_pos = pygame.math.Vector2(50, 1080 // 2)
        self._gameObject = GameObject(start_pos)
        
        self._gameObject.add_component(SpriteRenderer(Entities.PLAYER))
        
        animator = self._gameObject.add_component(Animator())
        animator.play_animation(Entities.PLAYER)
        
        self._gameObject.add_component(Collider())
        self._gameObject.add_component(Player())
    
    def get_gameObject(self) -> GameObject:
        return self._gameObject