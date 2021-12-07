import os
import yaml


def load_config(path=None):
    if not os.path.exists(path):
        return False
    return load(path, handler=yaml, Loader=yaml.FullLoader)


def load(path, mode="r", readlines=False, handler=None, **load_kwargs):
    try:
        with open(path, mode) as fh:
            if handler:
                return handler.load(fh, **load_kwargs)
            if readlines:
                return fh.readlines()
            return fh.read()
    except Exception as err:
        print("Failed to load file: {} - {}".format(path, err))
    return False
