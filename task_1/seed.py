from random import randint

import faker
import psycopg2
import psycopg2 as pg
from dotenv import dotenv_values

config = dotenv_values(".env")


def seed_data():
    with psycopg2.connect(
            dbname=config["PG_DB"],
            user=config["PG_USER"],
            password=config["PG_PASSWORD"],
            host=config["PG_HOST"],
    ) as con:
        try:
            cur = con.cursor()
            sql_to_status = """INSERT INTO status(name) VALUES (%s);"""
            statuses = [("new",), ("in progress",), ("completed",)]
            cur.executemany(sql_to_status, statuses)

            fake_data = faker.Faker()
            users = []
            for _ in range(100):
                users.append((fake_data.name(), fake_data.email()))
            sql_to_users = """INSERT INTO users(fullname,email) VALUES (%s,%s);"""
            cur.executemany(sql_to_users, users)

            tasks = []
            for _ in range(100):
                tasks.append(
                    (
                        fake_data.sentence(),
                        fake_data.sentence(),
                        str(randint(1, 3)),
                        str(randint(1, 100)),
                    )
                )
            sql_to_tasks = """INSERT INTO tasks(title,description,status_id,user_id) VALUES (%s,%s,%s,%s);"""
            cur.executemany(sql_to_tasks, tasks)

        except (Exception, pg.Error) as e:
            print(e)


if __name__ == "__main__":

    seed_data()
