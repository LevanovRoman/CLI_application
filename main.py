import time
import click

from connect_DB import *


SQL_command = """INSERT INTO users (surname, name, patronymic, data, gender)
             VALUES (?, ?, ?, ?, ?);"""
TITLE = ['Surname', 'Name', 'Patronymic', 'Data', 'Gender', 'Age']


@click.command()
@click.argument('number_arg', nargs=-1)
def main(number_arg):
    match number_arg[0]:
        case '1':
            create_db()
            print("Database has been created")
        case '2':
            _, *user_data = number_arg
            validate_data(user_data)
            refer_to_db(SQL_command, user_data)
            print('Entry was made to the database')
        case '3':
            sql_command = """SELECT DISTINCT * from users ORDER BY surname, name, patronymic;"""
            all_records = map(add_age, refer_to_db(sql_command))
            output_to_console(TITLE, all_records)
        case '4':
            for _ in range(100000):
                user_data = make_autofill()
                refer_to_db(SQL_command, user_data)
            for _ in range(100):
                surname, *data, _ = make_autofill()
                surname = 'F' + surname
                user_data = (surname, *data, 'male')
                refer_to_db(SQL_command, user_data)
        case '5':
            time_start = time.time()
            sql_command = """SELECT DISTINCT * from users WHERE gender = 'male' AND surname LIKE "F%";"""
            records = refer_to_db(sql_command)
            output_to_console(TITLE[:-1], records)
            time_end = time.time()
            print("Time to complete: ", time_end - time_start)
        case '666':
            sql_command = """DELETE FROM users"""
            refer_to_db(sql_command)


if __name__ == "__main__":
    main()