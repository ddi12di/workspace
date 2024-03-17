from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

db_host = getenv("DB_HOST")
db_name = getenv("DB_NAME")
db_user = getenv("DB_USER")
db_pass = getenv("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


