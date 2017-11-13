# coding=utf-8
import base_client
from datetime import datetime


class MyError(Exception):
    pass


class ClientGetID(base_client.BaseClient):
    # метод vk api
    method = "users"
    # GET, POST, ...
    http_method = "get"

    def __init__(self, username):
        # Инициализация
        super().__init__()
        self.json_data = None
        self.username = username

    def get_params(self):
        # Получение логина
        return {
            "user_ids": self.username
        }

    def response_handler(self, response):
        # Получение ID пользователя
        self.json_data = response.json()
        print(self.json_data)
        try:
            return self.json_data["response"][1]["uid"]

        except IndexError as err:
            raise MyError
            # raise SystemExit("Сервер не дает ответа на выражение json_data['response'][0]['uid']")

    def get_json(self):
        # Получить json строку
        return self.json_data


def calculate_age(born, today):
    # Вычисление возраста
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class ClientGetFriendsAges(base_client.BaseClient):
    # метод vk api
    method = "friends"
    # GET, POST, ...
    http_method = "get"

    def __init__(self, user_id):
        # Инициализация
        super().__init__()
        self.json_data = None
        self.user_id = user_id

    def get_params(self):
        return {
            "user_id": self.user_id,
            "fields": "bdate"
        }

    def response_handler(self, response):
        # Получение списка возрастов
        self.json_data = response.json()
        ages = list()
        today = datetime.utcnow()

        for friend in self.json_data["response"]:
            date_of_birth = friend.get("bdate")
            try:
                date_of_birth = datetime.strptime(date_of_birth, "%d.%m.%Y")
            except Exception:
                continue

            ages.append(calculate_age(date_of_birth, today))

        return ages

    def get_json(self):
        return self.json_data()