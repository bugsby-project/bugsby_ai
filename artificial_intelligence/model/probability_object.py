class ProbabilityObject:
    def __init__(self, probability: float):
        self._probability = probability

    @property
    def probability(self):
        return self._probability

    @probability.setter
    def probability(self, other):
        self._probability = other

    def to_json(self) -> dict:
        return {
            "probability": self._probability
        }
