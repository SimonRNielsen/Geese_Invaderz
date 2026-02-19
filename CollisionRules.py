from Enums import Entities

COLLISION_RULES = {
    Entities.PLAYER: {
        Entities.WALKING_GOOSE,
        Entities.AGGRO_GOOSE,
        Entities.FIREBALL,
        Entities.ENEMY_PROJECTILE,
    },

    Entities.PLAYER_PROJECTILE: {
        Entities.WALKING_GOOSE,
        Entities.AGGRO_GOOSE,
        Entities.GOOSIFER,
        Entities.OBERST,
    },

    Entities.FIREBALL: {
        Entities.PLAYER,
    },

    Entities.ENEMY_PROJECTILE: {
        Entities.PLAYER,
    },

    Entities.WALKING_GOOSE: {
        Entities.PLAYER,
        Entities.PLAYER_PROJECTILE,
    },

    Entities.AGGRO_GOOSE: {
        Entities.PLAYER,
        Entities.PLAYER_PROJECTILE,
    },

    Entities.GOOSIFER: {
        Entities.PLAYER_PROJECTILE,
    },

    Entities.OBERST: {
        Entities.PLAYER_PROJECTILE,
    },
}