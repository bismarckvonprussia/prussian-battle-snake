

class SnakeBrain(object):
    """docstring for SnakeBrain."""

    def __init__(self):
        self.boardHeight = None
        self.boardWidth = None

    def initialize(self, game_data):
        print("Initializing snake brain")
        self.boardWidth = game_data["board"]["width"]
        self.boardHeight = game_data["board"]["height"]

    def decideNextMove(self, game_data):
        pass

        return "right"
