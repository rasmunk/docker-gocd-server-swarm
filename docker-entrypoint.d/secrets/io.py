import os


def makedirs(path):
    try:
        os.makedirs(path)
        return True, "Created: {}".format(path)
    except Exception as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)
    return False, "Failed to create the directory path: {}".format(path)


def load(path, mode="r", readlines=False):
    try:
        with open(path, mode) as fh:
            if readlines:
                return fh.readlines()
            return fh.read(), ""
    except Exception as err:
        return False, "Failed to load file: {} - {}".format(path, err)
    return False, "Failed to load file: {}".format(path)


def remove(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True, "Removed file: {}".format(path)
    except Exception as err:
        return False, "Failed to remove file: {} - {}".format(path, err)
    return False, "Failed to remove file: {}".format(path)


def exists(path):
    return os.path.exists(path)


def chmod(path, mode, **kwargs):
    try:
        os.chmod(path, mode, **kwargs)
    except Exception as err:
        return False, "Failed to set permissions: {} on: {} - {}".format(
            mode, path, err
        )
    return True, "Set the path: {} with permissions: {}".format(path, mode)
