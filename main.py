from datetime import date, timedelta

from sqlalchemy import func, and_

from db import User, HeartRate, Session


def query_users(session: Session, min_age: int, gender: str, min_avg_heart_rate: float, date_from: date, date_to: date):
    avg_heart_rate_subquery = (
        session.query(
            HeartRate.user_id,
            func.avg(HeartRate.heart_rate).label('avg_heart_rate')
        )
        .filter(
            and_(
                HeartRate.timestamp >= date_from,
                HeartRate.timestamp <= date_to
            )
        )
        .group_by(HeartRate.user_id)
        .subquery()
    )

    query = (
        session.query(
            User.id,
            User.name,
            User.gender,
            User.age,
            avg_heart_rate_subquery.c.avg_heart_rate
        )
        .join(avg_heart_rate_subquery, User.id == avg_heart_rate_subquery.c.user_id)
        .filter(
            and_(
                User.age > min_age,
                User.gender == gender,
                avg_heart_rate_subquery.c.avg_heart_rate > min_avg_heart_rate
            )
        )
    )

    return query.all()


def query_for_user(session: Session, user_id, date_from, date_to):
    truncated_ts = func.date_trunc('hour', HeartRate.timestamp).label('hour_start')
    hourly_averages = session.query(
        truncated_ts,
        func.avg(HeartRate.heart_rate).label('avg_heart_rate')
    ).filter(
        HeartRate.user_id == user_id,
        HeartRate.timestamp >= date_from,
        HeartRate.timestamp <= date_to
    ).group_by(
        func.date_trunc('hour', HeartRate.timestamp)
    ).order_by(
        func.avg(HeartRate.heart_rate).desc()
    ).limit(10).all()
    return hourly_averages


def query_heart_rates_with_user_names(session: Session, date_from, date_to):
    heart_rates_with_user_names = session.query(
        User.name,
        HeartRate.timestamp,
        HeartRate.heart_rate
    ).join(
        HeartRate, User.id == HeartRate.user_id
    ).filter(
        HeartRate.timestamp >= date_from,
        HeartRate.timestamp <= date_to
    ).order_by(
        User.name,
        HeartRate.timestamp
    ).all()

    return heart_rates_with_user_names


if __name__ == "__main__":
    with Session() as session:
        date_from = date.today() - timedelta(days=5)
        date_to = date.today()

        users = query_users(session, 18, 'male', 65, date_from, date_to)
        print(f'query_users(18, \'male\', 65, {date_from}, {date_to}):')
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Gender: {user[2]}, Age: {user[3]}, Avg Heart Rate: {user[4]:.2f}")

        heart_rate_results = query_for_user(session, 1, date_from, date_to)
        print(f'\nquery_for_user(1, {date_from}, {date_to}):')
        for result in heart_rate_results:
            print(f"Hour Start: {result[0]}, Avg Heart Rate: {result[1]:.2f}")

        heart_rates_with_user_names = query_heart_rates_with_user_names(session, date_from, date_to)
        print("\nHeart Rates with User Names:")
        for user_name, timestamp, heart_rate in heart_rates_with_user_names:
            print(f"User: {user_name}, Timestamp: {timestamp}, Heart Rate: {heart_rate:.2f}")
