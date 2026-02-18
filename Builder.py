from abc import ABC, abstractmethod
from GameObject import GameObject
from Components import SpriteRenderer, Animator, Collider, Entity
from Enemy import Enemy
from Enums import Entities
from Player import Player
import random, pygame
from UI import Healthbar

class Builder(ABC):

    def __init__(self):
        super().__init__()

    @classmethod
    @abstractmethod
    def build(self):
        pass

    def get_gameObject(self) -> GameObject:
        pass

class PlayerBuilder(Builder):

    def __init__(self):
        super().__init__()

    def build(self):
        #Startposition: venstre side midt på skærmen
        start_pos = pygame.math.Vector2(50, 1080 // 2)
        self._gameObject = GameObject(start_pos)
        
        self._gameObject.add_component(SpriteRenderer(Entities.PLAYER))
        animator = self._gameObject.add_component(Animator())
        animator.play_animation(Entities.PLAYER)
        
        self._gameObject.add_component(Collider())
        self._gameObject.add_component(Player())

        entity = self._gameObject.add_component(Entity())
        entity.max_health = 100
        entity.health = 100
    
    def get_gameObject(self) -> GameObject:
        return self._gameObject
    
class EnemyBuilder(Builder):

    def __init__(self):
        super().__init__()

    def build(self, entity_type):
        self._gameObject = GameObject(pygame.math.Vector2(-1000,-1000))
        self._gameObject.add_component(SpriteRenderer(entity_type))
        animator = self._gameObject.add_component(Animator())
        animator.play_animation(entity_type)
        self._gameObject.add_component(Collider())
        enemy = self._gameObject.add_component(Enemy())
        enemy.set_value(entity_type)
        self._gameObject.destroy()

    def get_gameObject(self):
        return self._gameObject