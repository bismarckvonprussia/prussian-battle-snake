import random
from enemy_snake import EnemySnake

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
        self.size = None
        self.enemySnakes = []
        self.snakeId = None

        random.seed(1234)

    def initialize(self, game_data):
        print("Initializing snake brain")
        self.boardWidth = game_data["board"]["width"]
        self.boardHeight = game_data["board"]["height"]
        self.snakeId = game_data["you"]["id"]

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

    def eliminateCollision(self, occupiedSegments):
        nextLeft = Coordinate(self.head.x - 1, self.head.y)
        nextRight = Coordinate(self.head.x + 1, self.head.y)
        nextUp = Coordinate(self.head.x, self.head.y - 1)
        nextDown = Coordinate(self.head.x, self.head.y + 1)
        for segment in occupiedSegments:
            if nextLeft == segment:
                if "left" in self.possibleMoves: self.possibleMoves.remove("left")
            if nextRight == segment:
                if "right" in self.possibleMoves: self.possibleMoves.remove("right")
            if nextUp == segment:
                if "up" in self.possibleMoves: self.possibleMoves.remove("up")
            if nextDown == segment:
                if "down" in self.possibleMoves: self.possibleMoves.remove("down")

    def eliminateSelfCollision(self):
        self.eliminateCollision(self.body)

    def eliminateSnakeCollision(self):
        for enemySnake in self.enemySnakes:
            self.eliminateCollision(enemySnake.body)

    def eliminateLosingHeadOnCollision(self):
        for enemySnake in self.enemySnakes:
            if self.size > enemySnake.size: continue
            enemyHeadNextLeft = enemySnake.head
            dangerSegments = []
            dangerSegments.append(Coordinate(enemySnake.head.x - 1, enemySnake.head.y))
            dangerSegments.append(Coordinate(enemySnake.head.x + 1, enemySnake.head.y))
            dangerSegments.append(Coordinate(enemySnake.head.x, enemySnake.head.y - 1))
            dangerSegments.append(Coordinate(enemySnake.head.x, enemySnake.head.y + 1))
            self.eliminateCollision(dangerSegments)

    def decideNextMove(self, game_data):
        self.possibleMoves = ['up', 'down', 'left', 'right']
        self.head = Coordinate(game_data["you"]["body"][0]["x"], game_data["you"]["body"][0]["y"])

        print("My snake ID: {}".format(self.snakeId))

        # head included in the body
        self.body = []
        for segment in game_data["you"]["body"]:
            self.body.append(Coordinate(segment["x"], segment["y"]))
        self.size = len(self.body)

        self.enemySnakes = []
        for rawEnemeySnake in game_data["board"]["snakes"]:
            if rawEnemeySnake["id"] == self.snakeId: continue
            enemySnake = EnemySnake()
            enemySnake.snakeId = rawEnemeySnake["id"]
            enemySnake.head = Coordinate(rawEnemeySnake["body"][0]["x"], rawEnemeySnake["body"][0]["y"])
            enemySnake.body = []
            for segment in rawEnemeySnake["body"]:
                enemySnake.body.append(Coordinate(segment["x"], segment["y"]))
            enemySnake.size = len(enemySnake.body)
            self.enemySnakes.append(enemySnake)

        self.eliminateBoardEdgeCollision()
        self.eliminateSelfCollision()
        self.eliminateSnakeCollision()
        self.eliminateLosingHeadOnCollision()

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
