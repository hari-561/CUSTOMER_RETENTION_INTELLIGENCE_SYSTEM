from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine

URL = "mysql+pymysql://root:root@localhost:3306/cris"

engine = create_engine(URL)

Session = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


