class Modifier:
    @staticmethod
    def rigged(t: float):
        return abs(t)

    @staticmethod
    def wood(t: float):
        n = 5.
        k = 1 / n
        return n * (t % k)
