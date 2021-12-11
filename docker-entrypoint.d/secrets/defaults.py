import os
from secrets.utils import is_env_set

PACKAGE_NAME = "gocd-setup-secrets"


GO_PLUGINS_BUNDLED_DIR = "/godata"
GO_SECRET_DIR = "/gosecrets"
GO_SECRET_DB_FILE = "{}/secrets.yml".format(GO_SECRET_DIR)

# ENV variables
GO_PLUGINS_BUNDLED_DIR = "GO_PLUGINS_BUNDLED_DIR"
GO_SECRET_DIR = "GO_SECRET_DIR"
GO_SECRET_DB_FILE = "GO_SECRET_DB_FILE"

# Other constants
GOCD_SECRET_PLUGIN = "gocd-file-based-secrets-plugin.jar"


def get_secrets_dir_path():
    dir_path, msg = is_env_set(GO_SECRET_DIR)
    if not dir_path:

        return False, msg
    return True, ""


def get_secrets_file_name():
    secrets_name, msg = is_env_set(GO_SECRET_DB_FILE)
    if not secrets_name:
        return False, msg
    return True, ""


def get_secrets_db_path():
    dir_path, msg = get_secrets_dir_path()
    if not dir_path:
        return False, msg
    file_name, msg = get_secrets_file_name()
    if not file_name:
        return False, msg
    return os.path.join(dir_path, file_name), ""
