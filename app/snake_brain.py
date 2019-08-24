import random

class SnakeBrain(object):
    """docstring for SnakeBrain."""

    def __init__(self):
        # Game meta
        self.boardHeight = None
        self.boardWidth = None

        # Snake variables
        self.possibleMoves = None
        self.head = None
        self.body = []

    def initialize(self, game_data):
        print("Initializing snake brain")
        self.boardWidth = game_data["board"]["width"]
        self.boardHeight = game_data["board"]["height"]

        print("Board Width: {}".format(self.boardWidth))
        print("Board Height: {}".format(self.boardHeight))

    def eliminateBoardEdgeCollision(self):
        if self.head.x - 1 < 0:
            self.possibleMoves.remove("left")
        if self.head.x + 1 == self.boardWidth:
            self.possibleMoves.remove("right")
        if self.head.y - 1 < 0:
            self.possibleMoves.remove("up")
        if self.head.y + 1 == self.boardHeight:
            self.possibleMoves.remove("down")

    def eliminateSelfCollision(self):
        nextLeft = self.head.x - 1
        nextRight = self.head.x + 1
        nextUp = self.head.y - 1
        nextDown = self.head.y + 1
        for bodyPart in self.body:
            if nextLeft == bodyPart.x:
                if "left" in self.possibleMoves: self.possibleMoves.remove("left")
            if nextRight == bodyPart.x:
                if "right" in self.possibleMoves: self.possibleMoves.remove("right")
            if nextUp == bodyPart.y:
                if "up" in self.possibleMoves: self.possibleMoves.remove("up")
            if nextDown == bodyPart.y:
                if "down" in self.possibleMoves: self.possibleMoves.remove("down")

    def decideNextMove(self, game_data):
        self.possibleMoves = ['up', 'down', 'left', 'right']
        self.head = Coordinate(game_data["you"]["body"][0]["x"], game_data["you"]["body"][0]["y"])

        # head included in the body
        for segment in game_data["you"]["body"]:
            self.body.append(Coordinate(segment["x"], segment["y"]))

        self.eliminateBoardEdgeCollision()
        self.eliminateSelfCollision()

        if not self.possibleMoves:
            print("DOOM!!!")
            return "right"

        nextMove = random.choice(self.possibleMoves)
        return nextMove


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "{0},{1}".format(self.x, self.y)
