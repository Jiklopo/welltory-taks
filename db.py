from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

load_dotenv()
DATABASE_URL = getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    heart_rates = relationship("HeartRate", back_populates="user")


class HeartRate(Base):
    __tablename__ = 'heart_rates'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    timestamp = Column(DateTime)
    heart_rate = Column(Float)

    user = relationship("User", back_populates="heart_rates")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
