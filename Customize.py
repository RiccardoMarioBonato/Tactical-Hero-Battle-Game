import pygame


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (150, 150, 150)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    DARK_GRAY = (100, 100, 100)
    ORANGE = (255, 95, 31)
    LOCKED_COLOR = (150, 150, 150)


class Images:
    day_default = pygame.image.load("img/backgrounds/w6BZFE.jpg")
    night_default = pygame.image.load("img/backgrounds/night.png")
    swamp_default = pygame.image.load("img/backgrounds/Swamp_map.png")
    castle_default = pygame.image.load("img/backgrounds/Castle.png")
    slums_default = pygame.image.load("img/backgrounds/Slums.png")
    Future_default = pygame.image.load("img/backgrounds/Future.png")


class Resolution:
    WIDTH, HEIGHT = 1920, 1080
    FPS = 60


class Dimensions:
    BLOCK_SIZE1 = 40


class Hero:
    Lumberjack = pygame.image.load("Heros/LumberJack/LumberJack/LumberJack_final.png")
    lumberjack_photo = pygame.image.load("Heros/LumberJack/lumberjack_select_photo.webp")
    Pantheon = pygame.image.load("Heros/Pantheon/Pantheon/Pantheon_spritesheet.png")
    BrownBeard = pygame.image.load("Heros/BrownBeard/BrownBeard_Spritelist.png")
    Kitsune = pygame.image.load("Heros/Kitsune/Kitsune_spritesheet.png")
    Yamabushi_tengu = pygame.image.load("Heros/YamabushiTengu/Yamabushi_tengu_spritesheet.png")
    Karasu_tengu = pygame.image.load("Heros/KarasuTengu/Karasu_tengu_Spritesheet.png")
    SwordMaster = pygame.image.load("Heros/SwordMaster/Sword_Master_spritesheet.png")
    Convert = pygame.image.load("Heros/Converted/Converted_Vampire_Spritelist.png")
    Countess = pygame.image.load("Heros/Countess/Countess_Vampire_Spritelist.png")
    VampireGirl = pygame.image.load("Heros/VampireGirl/Vampire_Girl_Spritelist.png")
    Wanderer = pygame.image.load("Heros/Wanderer_Magican/Wanderer_Magican_Spritelist.png")
    LightMage = pygame.image.load("Heros/Light_Magican/Light_Mage_Spritelist.png")
    FireMage = pygame.image.load("Heros/Fire_magican/Fire_Mage_Spritelist.png")
    Gangster1 = pygame.image.load("Heros/Gangster1/Gangsters_1_Spritelist.png")
    Gangster2 = pygame.image.load("Heros/Gangster2/Gangsters_2_Spritelist.png")
    Gangster3 = pygame.image.load("Heros/Gangster3/Gangsters_3_Spritelist.png")
    Monk = pygame.image.load("Heros/Monk/Ninja_Monk_spritelist.png")
    Peasant = pygame.image.load("Heros/Ninja_Peasant/Ninja_Peasant_spritelist.png")
    Kunoichi = pygame.image.load("Heros/Kunoichi/Kunoichi_spritelist.png")


class Enemies:
    # lvl1
    GreenSlime = pygame.image.load("Enemies/Greenslime/Green_Slime_Spritelist.png")
    BlueSlime = pygame.image.load("Enemies/Blueslime/Blue_Slime_Spritelist.png")
    RedSlime = pygame.image.load("Enemies/Redslime/Red_Slime_Spritelist.png")
    # lv2
    RedWerewolf = pygame.image.load("Enemies/RedWerewolf/Red_Werewolf_Spritelist.png")
    GreyWerewolf = pygame.image.load("Enemies/GreyWerewolf/Grey_Werewolf_Spritelist.png")
    WhiteWerewolf = pygame.image.load("Enemies/WhiteWerewolf/White_Werewolf_Spritelist.png")
    # lv3
    Centipede = pygame.image.load("Enemies/Centipede/Centipede_SpriteSheet.png")
    Big_bloated = pygame.image.load("Enemies/Big_bloated/Big_bloated_spritesheet.png")
    Battle_turtle = pygame.image.load("Enemies/Battle_turtle/Battle_turtle_spritesheet.png")
    # lvl4
    Gargona1 = pygame.image.load("Enemies/Gargona1/Gargona_1_Spritelist.png")
    Gargona2 = pygame.image.load("Enemies/Gargona2/Gargona_2_Spritelist.png")
    Gargona3 = pygame.image.load("Enemies/Gargona3/Gargona_3_Spritelist.png")
    # lv5
    Homeless1 = pygame.image.load("Enemies/Homeless1/Homless_1_Spritelist.png")
    Homeless2 = pygame.image.load("Enemies/Homeless2/Homless_2_Spritelist.png")
    Homeless3 = pygame.image.load("Enemies/Homeless3/Homless_3_Spritelist.png")
    # lv6
    Destroyer = pygame.image.load("Enemies/Destroyer/Destroyer_spritelist.png")
    Infantry = pygame.image.load("Enemies/Infantry/Infantryman_spritelist.png")
    Swordsman = pygame.image.load("Enemies/Swordsman/Swordsman_spritelist.png")


class Projectile:
    Bullet = pygame.image.load("Enemies/Battle_turtle/Bullet1.png")  # add this line
    Bullet1 = pygame.image.load("Enemies/Battle_turtle/Bullet1.png")
    Bullet2 = pygame.image.load("Enemies/Battle_turtle/Bullet2.png")
    FireBullet = pygame.image.load("Heros/Countess/Blood_Charge_1.png")


class Fonts:
    pygame.font.init()
    ARIAL_16 = pygame.font.SysFont('Arial', 16)
    ARIAL_24 = pygame.font.SysFont('Arial', 24)
    ARIAL_32 = pygame.font.SysFont('Arial', 32)
    ARIAL_36 = pygame.font.SysFont('Arial', 36)
    ARIAL_48 = pygame.font.SysFont('Arial', 48)
    ARIAL_72 = pygame.font.SysFont('Arial', 72)

class Sound:
    background_music = pygame.mixer.music.load("Sounds/Background_music.mp3")