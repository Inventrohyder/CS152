class Literal:

    def __init__(self, name: str) -> None:
        self.name = name
        self.sign = True  # Initialize the literal sign as positive

    def __neg__(self) -> None:
        """Flip the sign of the Literal"""
        l = Literal(self.name)
        l.sign = not self.sign
        return l
        