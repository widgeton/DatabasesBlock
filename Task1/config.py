# это только пример, нужно вставить реальные данные
USER = "user"
PASSWORD = "password"
HOST = "localhost"
PORT = 5432
DB_NAME = "database"


def get_db_url():
    return f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
