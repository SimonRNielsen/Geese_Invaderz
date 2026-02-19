from Enums import Assets, Entities
import pygame

class AssetLoader:

    _animations = {}
    _sprites = {}

    @classmethod
    def get_animation_args(cls, asset_key):
        args = ()
        match asset_key:
            case Entities.PLAYER:
                args = ("player\\mortenMonk0.png",
                        "player\\mortenMonk1.png",
                        "player\\mortenMonk2.png",
                        "player\\mortenMonk3.png",
                        "player\\mortenMonk4.png",)
            case Entities.WALKING_GOOSE:
                args = ("enemy\\gooseWalk0.png",
                        "enemy\\gooseWalk1.png",
                        "enemy\\gooseWalk2.png",
                        "enemy\\gooseWalk3.png",
                        "enemy\\gooseWalk4.png",
                        "enemy\\gooseWalk5.png",
                        "enemy\\gooseWalk6.png",
                        "enemy\\gooseWalk7.png",)
            case Entities.OBERST:
                args = ("enemy\\OberstStille.png",
                        "enemy\\OberstSkyd.png",)
            case Entities.AGGRO_GOOSE:
                args = ("enemy\\aggro0.png",
                        "enemy\\aggro1.png",
                        "enemy\\aggro2.png",
                        "enemy\\aggro3.png",
                        "enemy\\aggro4.png",
                        "enemy\\aggro5.png",
                        "enemy\\aggro6.png",
                        "enemy\\aggro7.png",)
            case Entities.GOOSIFER:
                args = ("enemy\\goosifer0.png",
                        "enemy\\goosifer1.png",
                        "enemy\\goosifer2.png",)
            #case Entities.SHEEP:
                #args = ("enemy\\sheep.png",
                        #"enemy\\sheep.png",)
            case _:
                print(f"No match case for {asset_key} in get_animation_args")
                return None
        return args

    @classmethod
    def get_sprite_arg(cls, asset_key):
        match asset_key:
            case Entities.PLAYER:
                return "player\\mortenMonk0.png"
            case Entities.VARM_HVEDE:
                return "projectiles\\Varm_Hvede.png"
            case Entities.STEN_HVEDE:
                return "projectiles\\Sten_Hvede.png"
            case Entities.WALKING_GOOSE:
                return "enemy\\gooseWalk0.png"
            case Entities.OBERST:
                return "enemy\\OberstStille.png"
            case Entities.AGGRO_GOOSE:
                return "enemy\\aggro0.png"
            #case Entities.SHEEP:
                #return "enemy\\sheep.png"
            case Entities.GOOSIFER:
                return "enemy\\goosifer0.png"
            case Entities.FIREBALL:
                return "projectiles\\fireball.png"
            case Entities.PLAYER_PROJECTILE:
                return "projectiles\\hvede.png"
            case Entities.ENEMY_PROJECTILE:
                return "projectiles\\egg2.png"
            case Assets.START_MENU:
                return "menu\\startMenu.png"
            case Assets.WIN_SCREEN:
                return "menu\\winScreen.png"
            case Assets.LOOSE_SCREEN:
                return "menu\\looseScreen.png"
            case Assets.PAUSE:
                return "menu\\pause.png"
            case Assets.BUTTON:
                return "menu\\button.png"
            case Assets.BUTTON_PRESSED:
                return "menu\\buttonPressed.png"
            case Assets.BG_LEVEL_1:
                return  "Background\\Bg1.png"
            case Assets.BG_LEVEL_2:
                return  "Background\\Bg2.png"
            case Assets.BG_LEVEL_3:
                return  "Background\\Bg3.png"
            case Assets.BG_LEVEL_4:
                return  "Background\\Bg4.png"
            case _:
                print(f"No match case for {asset_key} in get_sprite_arg")
                return None
            
    @classmethod
    def get_animations(cls, asset_key):
        if asset_key not in cls._animations:
            args = cls.get_animation_args(asset_key)
            animation = []
            for arg in args:
                    sprite_image = pygame.image.load(f"assets\\{arg}")
                    animation.append(sprite_image)
            cls._animations[asset_key] = animation
        return cls._animations[asset_key]
    
    @classmethod
    def get_sprite(cls, asset_key):
        if asset_key not in cls._sprites:
            arg = cls.get_sprite_arg(asset_key)
            sprite = pygame.image.load(f"assets\\{arg}")
            cls._sprites[asset_key] = sprite
        return cls._sprites[asset_key]