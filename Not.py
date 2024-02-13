class Not:
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f"¬{self.formula}"
