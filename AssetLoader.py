from Customize import Hero, Enemies, Projectile
import json
import os


class AssetLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
            cls._instance.assets = {}
        return cls._instance

    def load_all_assets(self):
        if self._loaded:
            return

        # Load hero sprites
        self.assets['heroes'] = {
            'LumberJack': Hero.Lumberjack,
            'Pantheon': Hero.Pantheon,
            'BrownBeard': Hero.BrownBeard,
            'Kitsune': Hero.Kitsune,
            'YamabushiTengu': Hero.Yamabushi_tengu,
            'KarasuTengu': Hero.Karasu_tengu,
            'SwordMaster': Hero.SwordMaster,
            'Convert': Hero.Convert,
            'Countess': Hero.Countess,
            'VampireGirl': Hero.VampireGirl,
            'Wanderer': Hero.Wanderer,
            'LightMage': Hero.LightMage,
            'FireMage': Hero.FireMage,
            'Gangster1': Hero.Gangster1,
            'Gangster2': Hero.Gangster2,
            'Gangster3': Hero.Gangster3,
            'Monk': Hero.Monk,
            'Peasant': Hero.Peasant,
            'Kunoichi': Hero.Kunoichi,
        }

        # Load enemy sprites
        self.assets['enemies'] = {
            'Centipede': Enemies.Centipede,
            'BigBloated': Enemies.Big_bloated,
            'BattleTurtle': Enemies.Battle_turtle,
            'BlueSlime': Enemies.BlueSlime,
            'RedSlime': Enemies.RedSlime,
            'GreenSlime': Enemies.GreenSlime,
            'GreyWerewolf': Enemies.GreyWerewolf,
            'RedWerewolf': Enemies.RedWerewolf,
            'WhiteWerewolf': Enemies.WhiteWerewolf,
            'Gargona1': Enemies.Gargona1,
            'Gargona2': Enemies.Gargona2,
            'Gargona3': Enemies.Gargona3,
            'Homeless1': Enemies.Homeless1,
            'Homeless2': Enemies.Homeless2,
            'Homeless3': Enemies.Homeless3,
            'Destroyer': Enemies.Destroyer,
            'Infantry': Enemies.Infantry,
            'Swordsman': Enemies.Swordsman
        }

        # Load projectiles
        self.assets['projectiles'] = {
            'Bullet1': Projectile.Bullet1,
            'Bullet2': Projectile.Bullet2,
            'FireBullet': Projectile.Bullet2
        }

        # Load backgrounds (add to Customize.py if needed)
        self._loaded = True
        return self.assets


class UnitConfig:
    def __init__(self):
        self.config = self._load_config()

    @staticmethod
    def _load_config():
        config_path = os.path.join(os.path.dirname(__file__), 'unit_config.json')
        with open(config_path, 'r') as f:
            return json.load(f)

    def get_unit_config(self, unit_name):
        return self.config['units'].get(unit_name, None)
