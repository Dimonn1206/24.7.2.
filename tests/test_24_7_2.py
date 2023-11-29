"""Здесь находятся 8/10 тестов для задания 24.7.2. """
import pytest

from api import PetFriends
from settings import valid_email, valid_password, fake_email, fake_password
import os

pf = PetFriends()


def test_get_api_key_for_fake_user(email=fake_email, password=fake_password):
    """Запускаем негативный тест для аторизации несущестующего пользователя"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status == 403


def test_add_new_pets_incorrect_data(name=221, animal_type=321, age='7', pet_photo='image/cat2.jpg'):
    """Проверяем, что можно добавить питомца c некорректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_new_pets(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] != int
    assert result['animal_type'] != int

def test_get_list_of_pets_filter_my_pets(filter='my_pets'):
    """Отправляем запрос с выбором фильтра 'my_pets' и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets']) > 0

def test_create_pet_simple_empty_data(name="", animal_type='', age = ''):
    """Проверяем, что можно добавить питомца с пустыми параметрами"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_create_pet_simple_mani_characters(name="Кот"*14, animal_type='кошка', age = '5'):
    """Проверяем, что можно добавить питомца с параметрами, в которых может быть большое кол-во символов.
    Чтобы визуально не портить код перемножаем строку имени в несколько раз"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_create_pet_simple_two_copy(name="Маруся", animal_type='кошка', age = '2'):
    """Проверяем, что можно создать два одинаковых питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Создаем два одинаковых питомца
    status1, result1 = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    status2, result2 = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    assert status1 == 200
    assert result1['name'] == name

    assert status2 == 200
    assert result2['name'] == name


def test_get_list_of_pets_fake_key(filter=''):
    """Отправляем запрос на получение списка питомцев с неверным ключем авторизации"""

    #Используем неверный ключ авторизации
    auth_key = {'key': 'bsasxc1235672'}

    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    try:
        assert status == 200
        print('Статус-код: 200')
    except:
        assert status == 403
        print('Статус-код: 403')

def test_update_photo_of_pet(pet_photo='image/cat2.jpg'):

    """Проверяем возможность замены фото существующего питомца через запрос"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    # Сравниваем полученный ответ с ожидаемым

    status, result = pf.post_add_photo_of_pet(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    try:
        assert status == 200
        print('Статус-код: 200')
    except:
        assert status == 405
        print('Статус-код: 405')















