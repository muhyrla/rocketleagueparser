import configparser

config = configparser.ConfigParser()
config.read('db/itemdata-base.ini')


def searchitemid(name):
    id = None
    for key, value in config.items('ITEMS'):
        if value == name:
            id = key
            break

    if id is not None:
        return id
    else:
        return None
