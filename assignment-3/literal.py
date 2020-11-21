class Literal:

    def __init__(self, name: str) -> None:
        self.name = name
        self.sign = True  # Initialize the literal sign as positive

    def pure(self):
        """Gets the pure version of the Literal without any negative"""
        if self.sign:
            return self
        else:
            return -self

    def __neg__(self):
        """Flip the sign of the Literal"""
        l = Literal(self.name)
        l.sign = not self.sign
        return l

    def __lt__(self, other) -> bool:
        return self.name < other.name

    def __repr__(self) -> str:
        sign = "" if self.sign else "-"
        return f"{sign}{self.name}"

    def __eq__(self, o: object) -> bool:
        """Two literals are equal when their names are equal"""
        return self.name == o.name

    def __hash__(self) -> int:
        return self.name.__hash__()
