from os import getenv


def __load_environments_from_dot_env():
    from dotenv import load_dotenv

    load_dotenv(verbose=False)


__load_environments_from_dot_env()
NAVER_API_CLIENT_ID = getenv("NAVER_API_CLIENT_ID")
NAVER_API_CLIENT_SECRET = getenv("NAVER_API_CLIENT_SECRET")
MONGO_DB_URL = getenv("MONGO_DB_URL")
MONGO_DB_DATABASE_NAME = getenv("MONGO_DB_DATABASE_NAME")


def __create_logger():
    import logging

    _formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s")
    _handler = logging.StreamHandler()
    _handler.setFormatter(_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_handler)

    return logger


logger = __create_logger()
