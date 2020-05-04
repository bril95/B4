import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.String(36), primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Float)

class Athelete(Base):

    __tablename__ = "athelete"

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.String(36), primary_key=True)
    age= sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals =sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
    user_id = input("введите id пользователя: ")
    return int(user_id)

def convert_birthdate(data_format):
    data_split = data_format.split("-")
    data_int = map(int,data_split)
    date = datetime.date(*data_int)
    return date

def near_birthdate(user, session):
    athlete_birthdate = {}
    athlete_list = session.query(Athelete).all()
    for athlete in athlete_list:
        b_data = convert_birthdate(athlete.birthdate)
        athlete_birthdate[athlete.id] = b_data
    user_birthdate = convert_birthdate(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, b_data in athlete_birthdate.items():
        distans =abs(user_birthdate-b_data)
        if not min_dist or distans<min_dist:
            min_dist = distans
            athlete_id = id_
            athlete_bd = b_data
    return athlete_id, athlete_bd

def near_heigh(user, session):
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height

    return athlete_id, athlete_height

def main():
    session = connect_db()
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя не нашлось:(")
    else:
        bd_athlete, bd = near_birthdate(user, session)
        height_athlete, height = near_heigh(user, session)
        print("Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd))
        print("Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height))

if __name__ == "__main__":
    main()