from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Callback(Base):
	__tablename__ = "db1"

	user_id = Column(Integer, index=True)
	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String, index=True)
	body = Column(String, index=True)