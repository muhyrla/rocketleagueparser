import configparser

config = configparser.ConfigParser()


def searchitemid_withcategory(name, file):
    config.read(f'db/itemdata-base-{file}.ini')
    id = None
    for key, value in config.items('ITEMS'):
        if value == name:
            id = key
            break

    if id is not None:
        return id
    else:
        return None
