class RocketPart:
    def __init__(self, position, size, weight):
        self.position = position
        self.size = size
        self.weight = weight

class Engine(RocketPart):
    def __init__(self, position):
        super().__init__(position, (2,2), 1000)
        self.activated = False

class FuelTank(RocketPart):
    def __init__(self, position):
        super().__init__(position, (2,2), 1000)
        self.full = 1

class Separator(RocketPart):
    def __init__(self, position):
        super().__init__(position, (1,2), 200)
        self.activated = False

class Capsule(RocketPart):
    def __init__(self, position):
        super().__init__(position, (2,2), 200)
        self.activated = False