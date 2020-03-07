import platform

from utils.log import init_log

system = platform.system()

if system == "Linux":
    DEBUG = False
elif system == "Windows":
    DEBUG = True

logger = init_log()

DATABASES = {
    "debug": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "*",
        "database": "mysql",
        "use_unicode": True,
        "charset": "utf8mb4",
        "autocommit": True,
    },
    "product": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "*",
        "database": "mysql",
        "use_unicode": True,
        "charset": "utf8mb4",
        "autocommit": True,
    }
}

MONGO = {
    "debug": {
        "host": "127.0.0.1",
        "port": 27017,
        "user": "user",
        "passwd": "*",
    },
    "product": {
        "host": "127.0.0.1",
        "port": 27017,
        "user": "user",
        "passwd": "*",
    }
}
