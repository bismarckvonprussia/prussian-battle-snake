import json
import os
import random
import bottle
import argparse

from api import ping_response, start_response, move_response, end_response

from snake_brain import SnakeBrain

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print("Initial game state:")
    print(json.dumps(data))

    snake_brain.initialize(data)

    color = "#003153"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    # directions = ['up', 'down', 'left', 'right']
    # directions = ['right']
    # direction = random.choice(directions)

    direction = snake_brain.decideNextMove(data)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print("### end()")
    # print(json.dumps(data))

    print("##### GAME OVER #####")

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

snake_brain = SnakeBrain()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action="store", required=True)
    args = parser.parse_args()

    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', args.p),
        debug=os.getenv('DEBUG', True)
    )
