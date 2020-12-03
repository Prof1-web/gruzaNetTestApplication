from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine("postgresql://{}:{}@{}:5432/{}".format(
    os.getenv("DB_USERNAME"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_NAME")
), pool_size=5, max_overflow=10)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from apps.users import models as users_models

    Base.metadata.create_all(bind=engine)
    users_models.load_db_data(db_session)
    print("db inited succesfully")
