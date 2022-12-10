
class Body():

    def __init__(
        self,
        color: str,
        x: int = None,
        y: int = None,
        rad: int = None,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.rad = rad