from abc import ABC, abstractmethod
from Enums import Entities, Components
from Builder import EnemyBuilder

class ObjectPool(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_object(self, entity):
        pass

    @abstractmethod
    def return_object(self, entity):
        pass

class EnemyPool(ObjectPool):

    def __init__(self, game_world):
        super().__init__()
        self._game_world = game_world
        self._enemy_pool = []
        for i in range(4):
            builder = EnemyBuilder()
            builder.build(Entities.WALKING_GOOSE)
            object = builder.get_gameObject()
            self._enemy_pool.append(object)

            builder = EnemyBuilder()
            builder.build(Entities.AGGRO_GOOSE)
            object = builder.get_gameObject()
            self._enemy_pool.append(object)

    def return_object(self, entity):
        entity.destroy()
        self._enemy_pool.append(entity)

    def get_object(self, entity_type, position):
        self._enemy_pool = [obj for obj in self._enemy_pool if obj.is_destroyed]
        for entity in self._enemy_pool:
            if entity._entity_type == entity_type:
                entity.transform.position = position
                return entity
        builder = EnemyBuilder()
        builder.build(entity_type)
        object = builder.get_gameObject()
        object.transform.position = position
        return object