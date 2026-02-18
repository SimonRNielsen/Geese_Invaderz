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