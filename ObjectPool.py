from abc import ABC, abstractmethod
from Enums import Entities, GameEvents, Components, SFX
from Builder import EnemyBuilder, ProjectileBuilder

class ObjectPool(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_object(self, entity):
        pass

    @abstractmethod
    def return_object(self, entity_type, position):
        pass

class EnemyPool(ObjectPool):

    def __init__(self, game_world):
        super().__init__()
        self._game_world = game_world
        self._enemy_pool = []
        for i in range(4):
            builder = EnemyBuilder()
            builder.build(Entities.WALKING_GOOSE)
            self._enemy_pool.append(builder.get_gameObject())
            builder = EnemyBuilder()
            builder.build(Entities.AGGRO_GOOSE)
            self._enemy_pool.append(builder.get_gameObject())
            builder = EnemyBuilder()
            builder.build(Entities.SHEEP)
            self._enemy_pool.append(builder.get_gameObject())
        builder = EnemyBuilder()
        builder.build(Entities.GOOSIFER)
        self._enemy_pool.append(builder.get_gameObject())

    def return_object(self, entity):
        entity.destroy()
        self._enemy_pool.append(entity)
        self._game_world._events[GameEvents.ENEMY_DEATH](entity)

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
    
class ProjectilePool(ObjectPool):

    def __init__(self, game_world):
        super().__init__()
        self._game_world = game_world
        self._projectile_pool = []
        self._player_projectile_type = Entities.PLAYER_PROJECTILE
        self._player_projectile_damage = 1
        for i in range(10):
            builder = ProjectileBuilder()
            builder.build(Entities.ENEMY_PROJECTILE)
            self._projectile_pool.append(builder.get_gameObject())
            builder = ProjectileBuilder()
            builder.build(self._player_projectile_type)
            self._projectile_pool.append(builder.get_gameObject())
            builder = ProjectileBuilder()
            builder.build(Entities.FIREBALL)
            self._projectile_pool.append(builder.get_gameObject())

    def return_object(self, entity):
        entity.destroy()
        self._projectile_pool.append(entity)

    def get_object(self, entity_type, position):
        match entity_type: 
            case Entities.FIREBALL:
                self._game_world._sound_manager.play_sound(SFX.FIREBALL)
            case Entities.ENEMY_PROJECTILE:
                self._game_world._sound_manager.play_sound(SFX.ENEMY_SHOOT)
            case Entities.PLAYER_PROJECTILE:
                self._game_world._sound_manager.play_sound(SFX.PLAYER_SHOOT)
            case _:
                pass
        self._projectile_pool = [obj for obj in self._projectile_pool if obj.is_destroyed]
        for entity in self._projectile_pool:
            if entity._entity_type == entity_type:
                entity.transform.position = position
                return entity
        builder = ProjectileBuilder()
        builder.build(entity_type)
        object = builder.get_gameObject()
        if entity_type is Entities.PLAYER_PROJECTILE and self._player_projectile_type is not Entities.PLAYER_PROJECTILE:
            object.get_component(Components.SPRITERENDERER.value).change_sprite(self._player_projectile_type)
            object._damage = self._player_projectile_damage
        object.transform.position = position
        return object
    
    def upgrade_pooled_shots(self, upgraded_sprite, upgraded_damage):
        self._player_projectile_type = upgraded_sprite
        self._player_projectile_damage = upgraded_damage
        for projectile in self._projectile_pool:
            if projectile._entity_type is Entities.PLAYER_PROJECTILE:
                projectile.get_component(Components.SPRITERENDERER.value).change_sprite(self._player_projectile_type)
                projectile._damage = self._player_projectile_damage