from abc import ABC, abstractmethod
from Enums import Entities, GameEvents, Components, SFX
from Builder import EnemyBuilder, ProjectileBuilder
import random
import pygame

class ObjectPool(ABC): #Superclass for object pools

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
        for i in range(10): #Precreates 10 of each enemy except boss
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
        self._game_world.boss = builder.get_gameObject() #Defines boss in gameworld
        
    def set_allowed_enemies(self, enemies: list[Entities]):
        self._allowed_enemies = enemies
    
    def spawn_random_enemy(self):
        if not self._allowed_enemies:
            return
        
        enemy_type = random.choice(self._allowed_enemies)

        if self._game_world.boss_exists(): #Checks if boss is active, and prevents further spawns if so
            return
                
        pos= self.get_spawn_position(enemy_type)
        enemy = self.get_object_filtered(enemy_type, pos)
        if enemy:
            self._game_world.instantiate(enemy)

    def get_spawn_position(self, enemy_type): #Sets a random spawn position dependent on type
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
            x = screen_width + sprite_width
            y = random.randint(0, screen_height - sprite_height)
            return pygame.math.Vector2(x, y)
        
    def boss_wave_enemy(self): #Used by boss to rapidly spawn enemies on random locations
        pos= self.get_spawn_position(Entities.AGGRO_GOOSE)
        enemy = self.get_object(Entities.AGGRO_GOOSE, pos)
        if enemy:
            self._game_world.instantiate(enemy)

    def return_object(self, entity):
        entity.destroy()
        self._enemy_pool.append(entity) #Returns the enemy to the pool
        self._game_world.notify(GameEvents.ENEMY_DEATH, entity) #Notifies game world that a enemy was returned, and which kind

    def get_object_filtered(self, entity_type, position):
        
        if self._allowed_enemies and entity_type not in self._allowed_enemies:
            return None
        
        self._enemy_pool = [obj for obj in self._enemy_pool if obj.is_destroyed] #"Removes" objects from the pool that aren't destroyed
        for entity in self._enemy_pool: #Attempts to locate a match to the entity type and set position + return it
            if entity.entity_type == entity_type:
                entity.transform.position = position
                return entity
        builder = EnemyBuilder() #Starts creating a new enemy if no compatible were found
        builder.build(entity_type)
        object = builder.get_gameObject()
        object.transform.position = position
        return object

    def get_object(self, entity_type, position): #Same as above, but without tampering
                
        self._enemy_pool = [obj for obj in self._enemy_pool if obj.is_destroyed] #Removes objects from the pool that aren't destroyed
        for entity in self._enemy_pool: #Attempts to locate a match to the entity type and set position + return it
            if entity.entity_type == entity_type:
                entity.transform.position = position
                return entity
        builder = EnemyBuilder() #Starts creating a new enemy if no compatible were found
        builder.build(entity_type)
        object = builder.get_gameObject()
        object.transform.position = position
        return object
    
class ProjectilePool(ObjectPool):

    def __init__(self, game_world):
        super().__init__()
        self._game_world = game_world
        self._projectile_pool = []
        self._player_projectile_type = Entities.PLAYER_PROJECTILE #Default type of player projectiles
        self._player_projectile_damage = 1 #Default value for projectile damage
        for i in range(10): #Precreates 10 of each projectile type
            builder = ProjectileBuilder()
            builder.build(Entities.ENEMY_PROJECTILE)
            self._projectile_pool.append(builder.get_gameObject())
            builder.get_gameObject().awake(game_world)
            builder = ProjectileBuilder()
            builder.build(self._player_projectile_type)
            self._projectile_pool.append(builder.get_gameObject())
            builder = ProjectileBuilder()
            builder.build(Entities.FIREBALL)
            self._projectile_pool.append(builder.get_gameObject())

    def return_object(self, entity): #Returns object to pool, and sets parameters for removing from gameworlds pool
        entity.destroy()
        self._projectile_pool.append(entity)

    def get_object(self, entity_type, position): #Returns a projectile according to the desired type, and "spawns" it at the given position
        match entity_type: #Determines which SFX to play when "firing"
            case Entities.FIREBALL:
                self._game_world.sound_manager.play_sound(SFX.FIREBALL)
            case Entities.ENEMY_PROJECTILE:
                self._game_world.sound_manager.play_sound(SFX.ENEMY_SHOOT)
            case Entities.PLAYER_PROJECTILE:
                self._game_world.sound_manager.play_sound(SFX.PLAYER_SHOOT)
            case _:
                pass
        self._projectile_pool = [obj for obj in self._projectile_pool if obj.is_destroyed] #Removes objects already in use from pool
        for entity in self._projectile_pool: #Locates a matching type to retrieve
            if entity.entity_type == entity_type:
                entity.transform.position = position
                return entity
        builder = ProjectileBuilder() #Starts creating a new projectile
        builder.build(entity_type)
        object = builder.get_gameObject()
        if entity_type is Entities.PLAYER_PROJECTILE and self._player_projectile_type is not Entities.PLAYER_PROJECTILE: #Ensures the projectile is the correct type when a new is made
            object.get_component(Components.SPRITERENDERER.value).change_sprite(self._player_projectile_type)
            object.awake(self._game_world)
            object.damage = self._player_projectile_damage
        object.transform.position = position
        return object
    
    def upgrade_pooled_shots(self, upgraded_sprite, upgraded_damage): #Method to upgrade and set the type to the new input
        self._player_projectile_type = upgraded_sprite
        self._player_projectile_damage = upgraded_damage
        for projectile in self._projectile_pool: #Upgrades pooled projectiles
            if projectile.entity_type is Entities.PLAYER_PROJECTILE:
                projectile.get_component(Components.SPRITERENDERER.value).change_sprite(self._player_projectile_type)
                projectile.damage = self._player_projectile_damage
        for active in self._game_world.colliders: #Upgrades active projectiles
            if active.gameObject.entity_type is Entities.PLAYER_PROJECTILE:
                active.gameObject.get_component(Components.SPRITERENDERER.value).change_sprite(self._player_projectile_type)
                active.gameObject.damage = self._player_projectile_damage