import Enemy


class Levels:
    def __init__(self):
        self.level_number = 0
        self.units = []
        self.logic = Enemy.EnemyLogic()