from sqlalchemy import create_engine
from models.Base import Base

DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
