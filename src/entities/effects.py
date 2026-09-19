class EnemyEffect:
    def __init__(
        self, duration: float, stackable: bool = False, speed_multiplier: float = 1
    ):
        self.duration = duration
        self.duration_counter = 0

        self.stackable = stackable
        self.speed_multiplier = speed_multiplier

    def update(self, delta_time: float):
        self.duration_counter += delta_time


class FrozenEffect(EnemyEffect):
    duration = 0.5
    speed_multiplier = 0.5
    stackable = True

    def __init__(self):
        super().__init__(
            self.duration, stackable=self.stackable, speed_multiplier=self.speed_multiplier
        )
