import sqlite3 as sql
import random
import string
from re import split
from datetime import date, datetime
from re import fullmatch


DB_NAME = "user_data.db"
st = 'Correct data format: Surname Name Patronymic dd/mm/yyyy male(*or female)'
pattern = r'(0[1-9]|[12][0-9]|3[01])[- :/.](0[1-9]|1[012])[- :/.](19|20)\d\d'


class ValidationError(Exception):
    pass


def refer_to_db(sql_command, user_data=None):
    with sql.connect(DB_NAME) as connection:
        cur = connection.cursor()
        if user_data is None:
            cur.execute(sql_command)
            return cur.fetchall()
        else:
            cur.execute(sql_command, user_data)


def create_db():
    with sql.connect(DB_NAME) as connection:
        cur = connection.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
        surname TEXT NOT NULL,
        name TEXT NOT NULL,
        patronymic TEXT NOT NULL,      
        data TEXT NOT NULL,
        gender TEXT NOT NULL)   
        """)


def add_age(record: tuple):
    day, month, year = map(int, split(r'[.:;/,-]', record[3]))
    user_date = date(year, month, day)
    age = (date.today() - user_date).days//365
    return record + (str(age), )


def make_autofill():
    start = datetime(1940, 1, 1).timestamp()
    end = datetime(2000, 1, 1).timestamp()
    data = date.fromtimestamp(random.randrange(int(start), int(end))).strftime('%d-%m-%Y')
    gender = random.choice(['male', 'female'])
    fio = tuple(''.join(random.sample(string.ascii_lowercase, random.randint(2, 10))).capitalize() for _ in range(3))
    return fio + (data, gender)


def output_to_console(title, all_records):
    title = [inner.ljust(15) + '| ' for inner in title]
    output_records = [[inner.ljust(15) + '| ' for inner in outer] for outer in all_records]
    print(*title)
    print('-' * 105)
    for row in output_records:
        print(*row)
    print('-' * 105)


def validate_data(data):
    if len(data) < 5:
        raise ValidationError("Not enough data", st)
        # print("Not enough data", st, sep='\n')
    elif not all(i.isalpha() for i in data[:3]):
        print(data)
        raise ValidationError("Name should contain only letters", st)
    elif data[-1].lower() not in ('male', 'female'):
        raise ValidationError("Incorrect gender", st)
    elif fullmatch(pattern, data[3]) is None:
        raise ValidationError("Incorrect date of birth", st)
