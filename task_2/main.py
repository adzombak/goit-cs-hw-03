import pymongo
from pymongo import MongoClient


def connect_to_db():
    try:
        client = MongoClient(
            host=["localhost:27017"],
            username="user",
            password="pass",
        )
        return client.book
    except pymongo.errors.ConnectionFailure as e:
        print("Connection error: ", e)
        exit()


def print_result(result):
    print("-----Result-----")
    for el in result:
        print(el)
    print("----------------")


def read_from_db(db, name=None):
    result = []
    try:
        if name:
            result = db.cats.find({"name": name})
        else:
            result = db.cats.find({})
        print_result(result)
    except Exception as e:
        print("An exception occurred ::", e)


def update_age(db, name, age=None):
    if name and age:
        try:
            db.cats.update_one({"name": name}, {"$set": {"age": age}})
            result = db.cats.find_one({"name": name})
            print(result)
        except Exception as e:
            print("An exception occurred ::", e)


def add_feature(db, name, feature=None):
    if name and feature:
        try:
            db.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
            result = db.cats.find_one({"name": name})
            print(result)
        except Exception as e:
            print("An exception occurred ::", e)


def delete_records(db, name=None):
    try:
        if name:
            db.cats.delete_many({"name": name})
        else:
            db.cats.delete_many({})
        result = db.cats.find({})
        print_result(result)
    except Exception as e:
        print("An exception occurred ::", e)


def add_demo_records(db):
    try:
        result_many = db.cats.insert_many(
            [
                {
                    "name": "barsik",
                    "age": 3,
                    "features": ["ходить в капці", "дає себе гладити", "рудий"],
                },
                {
                    "name": "Lama",
                    "age": 2,
                    "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
                },
                {
                    "name": "Liza",
                    "age": 4,
                    "features": ["ходить в лоток", "дає себе гладити", "білий"],
                },
            ]
        )
    except Exception as e:
        print("An exception occurred ::", e)
    result = db.cats.find({})
    print_result(result)


def main():
    db = connect_to_db()

    while True:
        print("1. Read")
        print("2. Update: age")
        print("3. Update: Add feature")
        print("4. Delete")
        print("5. Add cats")
        print("0. Exit")
        action = input("Select: ")

        if action == "0":
            break
        elif action == "1":
            name = input("Enter Name: ")
            read_from_db(db, name)
        elif action == "2":
            name = input("Enter Name: ")
            age = input("New age: ")
            update_age(db, name, age)
        elif action == "3":
            name = input("Enter Name: ")
            feature = input("New feature: ")
            add_feature(db, name, feature)
        elif action == "4":
            name = input("Enter Name: ")
            delete_records(db, name)
        elif action == "5":
            add_demo_records(db)
        else:
            print("WRONG COMMAND. TRY AGAIN")


if __name__ == "__main__":
    main()
