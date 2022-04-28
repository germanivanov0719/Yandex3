import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()
from data import __all_models

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return None

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    print(f"Connecting to a database: {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)  # type: ignore


def create_session() -> Session:
    global __factory
    print("session made")
    if __factory is not None:
        return __factory()
    else:
        raise TypeError("Database was not initialized properly")
