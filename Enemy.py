from Components import Entity
from Enums import Entities

class Enemy(Entity):

    def __init__(self):
        super().__init__()

    def set_value(self, entity_type):
        self._gameObject._entity_type = entity_type
        match entity_type:
            case _:
                self._max_health = 1

    def awake(self, game_world):
        self._game_world = game_world
        self._gameObject._health = self._max_health
        self._gameObject._is_destroyed = False
    
    def start(self):
        pass

    def update(self, delta_time):
        pass

    def take_damage(self, value):
        self.gameObject._health -= value
        if self.gameObject._health <= 0:
            self._game_world._enemy_pool.return_object(self._gameObject)