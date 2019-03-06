import os
from configparser import ConfigParser


def config(filename='database_default.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default is postgresql
    # db is dict to hold key/value pairs of
    # connection parameters in ini file
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

        # Override default fake pguser and pgpasswrd
        env_pg_user = os.environ.get("AEKOS_PG_USER_ENV")
        env_pg_user_pswd = os.environ.get("PGPASSWORD")
        if env_pg_user_pswd and env_pg_user_pswd:
            db['user'] = env_pg_user
            db['password'] = env_pg_user_pswd
    else:
        raise Exception(f'Section {section} not found in the {filename} file!')
    return db


if __name__ == "__main__":
    db = config()
    print(db)
