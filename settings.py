import configparser
from textwrap import wrap

config = configparser.ConfigParser()
config.read('configuration.ini')

field = {}
for key in config['Field']:
    field[key] = int(config['Field'][key])

draw = {}
for key in config['Draw']:
    if key == 'font':
        draw[key] = config['Draw'][key]
        continue
    try:
        draw[key] = int(config['Draw'][key])
    except ValueError:
        try:
            draw[key] = {'True': True, 'False': False}[config['Draw'][key]]
        except KeyError:
            raise ValueError(f'({key} = {config["Draw"][key]}): {key} should be True or False')

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

