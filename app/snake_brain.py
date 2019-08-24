import random

class SnakeBrain(object):
    """docstring for SnakeBrain."""

    def __init__(self):
        self.debug = True
        # Game meta
        self.boardHeight = None
        self.boardWidth = None

        # Snake variables
        self.turnsDoomed = 0
        self.possibleMoves = None
        self.head = None
        self.body = None
        self.enemySnakes = []
        self.snakeId = None

    def initialize(self, game_data):
        print("Initializing snake brain")
        self.boardWidth = game_data["board"]["width"]
        self.boardHeight = game_data["board"]["height"]
        self.snakeId = game_data["you"]["id"]

        print("Board Width: {}".format(self.boardWidth))
        print("Board Height: {}".format(self.boardHeight))

    def eliminateBoardEdgeCollision(self):
        print("*** eliminateBoardEdgeCollision")
        if self.head.x - 1 < 0:
            self.possibleMoves.remove("left")
            print("eliminate left")
        if self.head.x + 1 == self.boardWidth:
            self.possibleMoves.remove("right")
            print("eliminate right")
        if self.head.y - 1 < 0:
            self.possibleMoves.remove("up")
            print("eliminate up")
        if self.head.y + 1 == self.boardHeight:
            self.possibleMoves.remove("down")
            print("eliminate down")

    def eliminateSelfCollision(self):
        print("*** eliminateSelfCollision")
        nextLeft = Coordinate(self.head.x - 1, self.head.y)
        nextRight = Coordinate(self.head.x + 1, self.head.y)
        nextUp = Coordinate(self.head.x, self.head.y - 1)
        nextDown = Coordinate(self.head.x, self.head.y + 1)
        print("nextLeft: {}".format(str(nextLeft)))
        print("nextRight: {}".format(str(nextRight)))
        print("nextUp: {}".format(str(nextUp)))
        print("nextDown: {}".format(str(nextDown)))
        for bodyPart in self.body:
            if nextLeft == bodyPart:
                if "left" in self.possibleMoves: self.possibleMoves.remove("left")
                print("eliminate left")
            if nextRight == bodyPart:
                if "right" in self.possibleMoves: self.possibleMoves.remove("right")
                print("eliminate right")
            if nextUp == bodyPart:
                if "up" in self.possibleMoves: self.possibleMoves.remove("up")
                print("elminate up")
            if nextDown == bodyPart:
                if "down" in self.possibleMoves: self.possibleMoves.remove("down")
                print("eliminate down")

        if not self.possibleMoves:
            for bodyPart in self.body:
                print(str(bodyPart))

    def eliminateSnakeCollision(self):
        print("*** eliminateSnakeCollision")
        # TODO: handle head on collisions
        # heads of enemy snakes are special case...
        nextLeft = Coordinate(self.head.x - 1, self.head.y)
        nextRight = Coordinate(self.head.x + 1, self.head.y)
        nextUp = Coordinate(self.head.x, self.head.y - 1)
        nextDown = Coordinate(self.head.x, self.head.y + 1)
        for enemySnakeBody in self.enemySnakes:
            for bodyPart in enemySnakeBody:
                if nextLeft == bodyPart:
                    if "left" in self.possibleMoves: self.possibleMoves.remove("left")
                    print("eliminate left")
                if nextRight == bodyPart:
                    if "right" in self.possibleMoves: self.possibleMoves.remove("right")
                    print("eliminate right")
                if nextUp == bodyPart:
                    if "up" in self.possibleMoves: self.possibleMoves.remove("up")
                    print("elminate up")
                if nextDown == bodyPart:
                    if "down" in self.possibleMoves: self.possibleMoves.remove("down")
                    print("eliminate down")

    def decideNextMove(self, game_data):
        self.possibleMoves = ['up', 'down', 'left', 'right']
        self.head = Coordinate(game_data["you"]["body"][0]["x"], game_data["you"]["body"][0]["y"])

        print("My snake ID: {}".format(self.snakeId))

        # head included in the body
        self.body = []
        for segment in game_data["you"]["body"]:
            self.body.append(Coordinate(segment["x"], segment["y"]))

        self.enemySnakes = []
        for enemySnake in game_data["board"]["snakes"]:
            if enemySnake["id"] == self.snakeId: continue
            enemySnakeBody = []
            print("enemyId: {}".format(enemySnake["id"]))
            print("enemySnake")
            print(enemySnake["body"])
            for segment in enemySnake["body"]:
                enemySnakeBody.append(Coordinate(segment["x"], segment["y"]))
            self.enemySnakes.append(enemySnakeBody)

        self.eliminateBoardEdgeCollision()
        self.eliminateSelfCollision()
        self.eliminateSnakeCollision()

        print("Head: " + str(self.head))

        if not self.possibleMoves:
            self.turnsDoomed += 1
            print("DOOM!!! {0}".format(self.turnsDoomed))
            return "right"

        nextMove = random.choice(self.possibleMoves)
        return nextMove


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "{0},{1}".format(self.x, self.y)
