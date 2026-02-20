from Enums import Entities, Assets, Components

LEVELS = [
    {
        "bg" : Assets.BG_LEVEL_1,
        "enemies" : [Entities.WALKING_GOOSE],
        "duration" : 30,
        "player_modifiers" : {
            "speed" : 400,
            "shoot_cooldown" : 0.45,
            "projectile_type" : Entities.PLAYER_PROJECTILE,
            "projectile_speed" : 600,
            "projectile_damage" : 1,
        }
    },

    {
        "bg" : Assets.BG_LEVEL_2,
        "enemies" : [Entities.OBERST],
        "duration" : 35,
        "player_modifiers" : {
            "speed" : 420,
            "shoot_cooldown" : 0.40,
            "projectile_type" : Entities.VARM_HVEDE,
            "projectile_speed" : 610,
            "projectile_damage" : 2,
        }
    },

    {
        "bg" : Assets.BG_LEVEL_3,
        "enemies" : [Entities.AGGRO_GOOSE],
        "duration" : 40,
        "player_modifiers" : {
            "speed" : 450,
            "shoot_cooldown" : 0.37,
            "projectile_type" : Entities.VARM_HVEDE,
            "projectile_speed" : 610,
            "projectile_damage" : 2,
        }
    },

    {
        "bg" : Assets.BG_LEVEL_4,
        "enemies" : [Entities.GOOSIFER],
        "duration" : None,
        "player_modifiers" : {
            "speed" : 455,
            "shoot_cooldown" : 0.35,
            "projectile_type" : Entities.STEN_HVEDE,
            "projectile_speed" : 620,
            "projectile_damage" : 3,
        }
    },
    

]

class LevelManager:
    def __init__(self, game_world):
        self._gw = game_world
        self._current_level = 0
        self._time_left = 0
        self._active = False

        #Enemy spawning
        self._spawn_timer = 0
        self._spawn_interval = 2
    
    @property
    def active_bool(self):
        return self._active
    
    @active_bool.setter
    def active_bool(self, value):
        self._active = value


    def start_level(self):
        level = LEVELS[self._current_level]
        self._active = True

        #Background
        self._gw.set_background(level["bg"])

        #Timer
        if level["duration"] is not None:
            self._time_left = level["duration"]
            self._gw.ui_timer.start(self._time_left)
            self._gw.enemy_kill_counter.start()
        else:
            self._time_left = None
            self._gw.ui_timer.hide()
            self._gw.enemy_kill_counter.hide()
        
        #Enemy spawning setup
        self._gw._enemy_pool.set_allowed_enemies(level["enemies"])

        #Apply player modifiers
        if "player_modifiers" in level:
            player_component = self._gw._player.get_component(Components.PLAYER.value)
            if player_component:
                player_component.apply_level_modifiers(level["player_modifiers"])
    
    def update(self, delta_time):
        if not self._active:
            return
        
        if self._time_left is not None:
            self._time_left -= delta_time
            self._gw.ui_timer.set_time(self._time_left)

            if self._time_left <= 0:
                self.next_level()
        
        self._spawn_timer += delta_time
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_timer = 0
            self._gw._enemy_pool.spawn_random_enemy()
    
    def next_level(self):
        self._current_level += 1

        if self._current_level >= len(LEVELS):
            self._gw.player_alive.is_destroyed = True
            self._active = False
            return #Game done(Win/Lose Screen)
        
        self.start_level()
    
    def boss_killed(self):
        self._gw.show_win_screen()
    
    def player_died(self):
        self._gw.show_loose_screen()

    def reset_level_to_zero(self):
        self._current_level = 0