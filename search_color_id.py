import configparser

config = configparser.ConfigParser()
config.read('db/colordata-base.ini')


def searchcolorid(name):
    id = None
    for key, value in config.items('COLORS'):
        if value == name:
            id = key
            break

    if id is not None:
        return id
    else:
        return None
