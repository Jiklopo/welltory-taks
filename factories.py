import random

import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from sqlalchemy import orm

from db import User, HeartRate, engine

fake = Faker()

Session = orm.scoped_session(orm.sessionmaker(bind=engine))
session = Session()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    id = factory.Sequence(int)
    name = factory.LazyAttribute(lambda _: fake.name())
    gender = factory.LazyAttribute(lambda _: random.choice(['male', 'female']))
    age = factory.LazyAttribute(lambda _: random.randint(18, 70))


class HeartRateFactory(SQLAlchemyModelFactory):
    class Meta:
        model = HeartRate
        sqlalchemy_session = session

    id = factory.Sequence(int)
    user_id = factory.SubFactory(UserFactory)
    timestamp = factory.LazyFunction(lambda: fake.date_time_between(start_date='-5d', end_date='now'))
    heart_rate = factory.LazyAttribute(lambda _: random.uniform(60, 100))


def generate_test_data(num_users=5, heart_rates_per_user=15):
    users = UserFactory.create_batch(num_users)
    for user in users:
        HeartRateFactory.create_batch(heart_rates_per_user, user_id=user.id)
    session.commit()


if __name__ == '__main__':
    generate_test_data()
