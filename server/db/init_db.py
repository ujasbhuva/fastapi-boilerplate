from server.db.base_class import Base
from server.db.session import engine


def init_db():
    print("____creating database_________")
    Base.metadata.create_all(engine)
    print("______database created________")
