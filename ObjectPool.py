from abc import ABC, abstractmethod
from Enums import Entities, GameEvents, Components, SFX
from Builder import EnemyBuilder, ProjectileBuilder
import random
import pygame

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
        self._allowed_enemies = []
        for i in range(4):
            builder = EnemyBuilder()
            builder.build(Entities.WALKING_GOOSE)
            self._enemy_pool.append(builder.get_gameObject())
            builder = EnemyBuilder()
            builder.build(Entities.AGGRO_GOOSE)
            self._enemy_pool.append(builder.get_gameObject())
            builder = EnemyBuilder()
            builder.build(Entities.OBERST)
            self._enemy_pool.append(builder.get_gameObject())
        builder = EnemyBuilder()
        builder.build(Entities.GOOSIFER)
        self._enemy_pool.append(builder.get_gameObject())
        
    def set_allowed_enemies(self, enemies: list[Entities]):
        self._allowed_enemies = enemies
    
    def spawn_random_enemy(self):
        if not self._allowed_enemies:
            return
        
        enemy_type = random.choice(self._allowed_enemies)

        if enemy_type == Entities.GOOSIFER:
            for obj in self._game_world._gameObjects:
                if getattr(obj, "_entity_type", None) == Entities.GOOSIFER:
                    return
                
        pos= self.get_spawn_position(enemy_type)
        enemy = self.get_object(enemy_type, pos)
        if enemy:
            self._game_world.instantiate(enemy)

        #y = random.randint(50, self._game_world.screen.get_height() - 100)
        #pos = pygame.math.Vector2(
        #    self._game_world.screen.get_width() + 50,
        #    y
        #)

        #self._game_world.spawn_enemy(enemy_type, pos)
    def get_spawn_position(self, enemy_type):
        screen_width = self._game_world.screen.get_width()
        screen_height = self._game_world.screen.get_height()

        sprite_height = 200
        sprite_width = 50
    
        if enemy_type == Entities.OBERST:
            #Spawn på højre kant, tilfældig Y
            x = int(screen_width * 1.1)
            y = random.randint(0, screen_height - sprite_height)
            return pygame.math.Vector2(x, y)
        else:
            #Default spawn
            x = screen_width + 50
            y = random.randint(0, screen_height - sprite_height)
            return pygame.math.Vector2(x, y)

    def return_object(self, entity):
        entity.destroy()
        self._enemy_pool.append(entity)
        self._game_world._events[GameEvents.ENEMY_DEATH](entity)

    def get_object(self, entity_type, position):
        
        if self._allowed_enemies and entity_type not in self._allowed_enemies:
            return None
        
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
        for active in self._game_world._colliders:
            if active.gameObject._entity_type is Entities.PLAYER_PROJECTILE:
                active.gameObject.get_component(Components.SPRITERENDERER.value).change_sprite(self._player_projectile_type)
                active._damage = self._player_projectile_damage