from Components import Entity, Collider
from Enums import Entities, Components, Collisions

class Enemy(Entity):

    def __init__(self):
        super().__init__()

    def set_value(self, entity_type):
        self._gameObject._entity_type = entity_type
        match entity_type:
            case _:
                self._max_health = 0

    def awake(self, game_world):
        self._game_world = game_world
        self._gameObject._health = self._max_health
        self._gameObject._is_destroyed = False
    
    def start(self):
        collider = self.gameObject.get_component(Components.COLLIDER.value)
        collider.subscribe(Collisions.PIXEL_ENTER, self.take_damage)

    def update(self, delta_time):
        pass

    def take_damage(self, collider):
        gameObject = collider.gameObject
        if gameObject._entity_type == Entities.FIREBALL:
            if self.gameObject._health <= 0:
                self._game_world._enemy_pool.return_object(self._gameObject)