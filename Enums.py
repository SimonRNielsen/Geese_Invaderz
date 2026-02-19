from enum import Enum, auto

class Collisions(Enum):
    ENTER = auto()
    EXIT = auto()
    PIXEL_ENTER = auto()
    PIXEL_EXIT = auto()

class Components(Enum):
    SPRITERENDERER = "SpriteRenderer"
    COLLIDER = "Collider"
    ANIMATOR = "Animator"
    ENEMY = "Enemy"
    PLAYER = "Player"
    ENTITY = "Entity"

class Assets(Enum):
    START_MENU = "Start"
    WIN_SCREEN = "Win"
    LOOSE_SCREEN = "Loose"
    BUTTON = "Button"
    BUTTON_PRESSED = "Button pressed"
    PAUSE = "Pause"

class Entities(Enum):
    PLAYER = "Player"
    WALKING_GOOSE = "Walking_Goose"
    AGGRO_GOOSE = "Aggro_Goose"
    GOOSIFER = "Goosifer"
    FIREBALL = "Fireball"
    SHEEP = "Sheep"
    PLAYER_PROJECTILE = "Player_Projectile"
    ENEMY_PROJECTILE = "Enemy_Projectile"
    UNKNOWN = ""

class Button_Types(Enum):
    START = "Start"
    EXIT = "Exit"
    RESTART = "Restart"
    RESUME = "Resume"
    MAIN = "Main menu"
    # EXIT_PAUSE = "Exit pause"

class GameEvents(Enum):
    ENEMY_DEATH = auto()
    PLAYER_DEATH = auto()
    ENEMY_ESCAPED = auto()
    MAIN = auto()

class Music(Enum):
    MENU = "assets\\sfx\\music\\menu.mp3"
    BOSSFIGHT = "assets\\sfx\\music\\boss_fight.mp3"

class SFX(Enum):
    PLAYER_TAKES_DAMAGE = "assets\\sfx\\sounds\\morten_Av.wav"
    PLAYER_WALK_ONE = "assets\\sfx\\sounds\\walkSound.wav"
    PLAYER_WALK_TWO = "assets\\sfx\\sounds\\walkSound2.wav"
    BUTTON_CLICK = "assets\\sfx\\sounds\\click.mp3"
    PLAYER_SHOOT = "assets\\sfx\\sounds\\slingshoot.mp3"
    ENEMY_SHOOT = "assets\\sfx\\sounds\\shootSound.wav"
    ENEMY_HONK = "assets\\sfx\\sounds\\gooseSound_Short.wav"
    EGG_SMASH = "assets\\sfx\\sounds\\eggSmashSound.wav"
    SHEEP = "assets\\sfx\\sounds\\sheep.mp3"
    FIREBALL = "assets\\sfx\\sounds\\fire-sound.mp3"
    FIRE_HIT = "assets\\sfx\\sounds\\fire_hit.mp3"
    HVEDE = "assets\\sfx\\sounds\\hvede.mp3"