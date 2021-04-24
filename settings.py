import configparser
from textwrap import wrap

config = configparser.ConfigParser()
config.read('configuration.ini')

colors = {}
for key in config['Colors']:
    color = config['Colors'][key]
    if color in config['Colors list']:
        color = config['Colors list'][color]
    color = color[1:]
    try:
        key = int(key)
    except ValueError:
        pass
    color = tuple(map(lambda x: int(x, 16), wrap(color, 2)))
    colors[key] = color

field = {}
for key in config['Field']:
    field[key] = int(config['Field'][key])
