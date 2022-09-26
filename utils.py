"""Возвращает всех пользователей"""
import json


def get_all_users():
    with open('Users.json', 'rt', encoding='UTF-8') as file:
        return json.load(file)


"""Возвращает все заказы"""


def get_all_order():
    with open('order.json', 'rt', encoding='UTF-8') as file:
        return json.load(file)


"""Возвращает все предложения"""


def gel_all_offer():
    with open('offer.json', 'rt', encoding='UTF-8') as file:
        return json.load(file)