
class Body():

    def __init__(
        self,
        type: str = None,
        color: str = None,
        x: int = None,
        y: int = None,
        rad: int = None,
        speed: int = None,
    ):
        self.type = type
        self.x = x
        self.y = y
        self.color = color
        self.rad = rad
        self.speed = speed
        self.randMove = True