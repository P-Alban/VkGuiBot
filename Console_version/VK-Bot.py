# coding: utf8
import sys
from getpass import getpass
from itertools import cycle
from time import sleep

import progressbar
import vk
from clint.textui import progress
from colorama import init
from termcolor import colored


def auth():
    """login vk"""
    global vk_api
    try:
        print('''
        1. Использовать своё приложение
        2. Использовать стандартное приложение
        ''')

        app = int(input('Ваш выбор: '))
        if app == 1:
            input_id = int(input('App ID: '))
            app_id = input_id
        elif app == 2:
            app_id = 5868794
        else:
            print(colored('Ошибка', 'red'))
            auth()

        login_vk = input('Введите ваш логин: ')
        password_vk = getpass('Введите ваш пароль: ')
        try:
            session = vk.AuthSession(
                app_id=app_id,
                user_login=login_vk,
                user_password=password_vk,
                scope='wall, messages, friends, groups, video'
            )

            vk_api = vk.API(session)
            print(colored('Авторизация прошла успешно', 'green'))
            choice_menu()
        except Exception:
            print(colored('Ошибка авторизации', 'red'))
            auth()

    except Exception:
        input('Нажмите Enter для выхода...')


def choice_menu():
    """menu"""
    print(colored('''
    1. Бот для груп
    2. Бот для сообщений
    3. Бот для друзей
    4. Очистить список групп
    5. Очистить список друзей
    6. Очистить список сообщений
    7. Очистить стену
    8. Выход
    9. Обратная связь''', 'yellow'))
    choice = int(input('Ваш выбор: '))
    if choice == 1:
        groups_flood_bot()
        return_menu()
    elif choice == 2:
        message_flood()
        return_menu()
    elif choice == 3:
        add_friends()
        return_menu()
    elif choice == 4:
        delete_all_groups()
        return_menu()
    elif choice == 5:
        delete_all_friends()
        return_menu()
    elif choice == 6:
        clear_message()
        return_menu()
    elif choice == 7:
        clear_wall()
        return_menu()
    elif choice == 8:
        input('Нажмите Enter для выхода...')
    elif choice == 9:
        update()
        return_menu()
    else:
        print(colored('Опция не найдена или сессия оборвана', 'red'))
        print('''
        1. Пройти авторизацию заново
        2. Открыть главное меню
        ''')

        choice = int(input('Ваш выбор: '))
        if choice == 1:
            auth()
        elif choice == 2:
            choice_menu()


def groups_flood_bot():
    """bot for groups flood"""
    init()
    choice = int(input('1 - Искать группы по категориям, '
                       '2 - Список групп из файла: '))
    if choice == 1:
        category = input('Введите категорию: ')
        find_group = vk_api.groups.search(q=category, type='group', count=1000)
        print(colored('Найдено {} групп'.format(find_group[0]), 'green'))

        message_for_flood = input('Введите сообщение: ')
        set_time = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))
        for group_id in find_group[1:]:  # Start Flood
            try:
                print('Постим в: ID ', group_id['gid'])
                vk_api.wall.post(owner_id=-group_id['gid'],
                                 message=message_for_flood)
                for _ in progress.bar(range(set_time)):
                    sleep(1)
                print(colored('Сообщение доставлено.', 'green'))
            except Exception:
                print(colored('Сообщение не доставлено.', 'red'))
                sleep(0.3)
    elif choice == 2:
        path = input('Файл: ')
        delay = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))
        message = input('Введите сообщение: ')
        with open(path, 'r') as f:
            for i in cycle(f):
                try:
                    print('Постим в: ID {}'.format(i))
                    vk_api.wall.post(owner_id=-int(i), message=message)
                    for _ in progress.bar(range(delay)):
                        sleep(1)
                    print(colored('Сообщение доставлено', 'green'))
                except Exception:
                    print(colored('Сообщение не доставлено', 'red'))
                    sleep(1)


def message_flood():
    """bot for message flood"""
    start_age = int(input('Минимальный возраст: '))
    end_age = int(input('Максимальный возраст: '))
    sex = int(input('Пол [1 - Женский, 2 - Мужской, 0 - Любой]: '))
    online = int(input('Онлайн [1 - искать только пользователей онлайн, 0 - любых]: '))
    message = input('Введите сообщение: ')
    delay = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))

    search_users = vk_api.users.search(
        age_from=start_age,
        age_to=end_age,
        sex=sex,
        online=online,
        sort=1,
        count=1000,
    )
    print(colored('Найдено {} пользователей'.format(search_users[0]), 'green'))
    for find_user in search_users[1:]:
        try:
            print('Отправляем сообщение {} {} ID --> {}'.format(
                find_user['first_name'],
                find_user['last_name'],
                find_user['uid']
            ))

            vk_api.messages.send(user_id=find_user['uid'], message=message)
            for _ in progress.bar(range(delay)):
                sleep(1)
            print(colored('Сообщение доставлено', 'green'))
        except Exception:
            print(colored('Сообщение не доставлено', 'red'))
            sleep(0.3)


def add_friends():
    '''bot for add friends'''
    min_age = int(input('Минимальный возраст: '))
    max_age = int(input('Максимальный возраст: '))
    sex = int(input('Пол [1 - Женский, 2 - Мужской, 0 - Любой]: '))
    online = int(input('Онлайн [1 - искать пользователей онлайн, 0 - любых]: '))
    delay = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))

    search_users = vk_api.users.search(
        age_from=min_age,
        age_to=max_age,
        sex=sex,
        sort=1,
        online=online,
        count=1000,
    )
    for find_friends in search_users[1:]:
        try:
            print('Отправляем заявку {} {} ID --> {}'.format(
                find_friends['first_name'], find_friends['last_name'],
                find_friends['uid']))
            vk_api.friends.add(user_id=find_friends['uid'])
            for _ in progress.bar(range(delay)):
                sleep(1)
            print(colored('Заявка отправлена', 'green'))
        except Exception:
            print(colored('Заявка не отправлена', 'red'))
            sleep(0.3)


def delete_all_groups():
    """bot for delete groups"""
    find_groups = vk_api.groups.get(count=1000)
    print(colored('Найдено {} групп', 'green').format(find_groups[0]))

    choice = input('Старт? [Y,n]: ')
    if choice == 'Y':
        print(colored('Подождите...', 'yellow'))
        bar_index = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for group_id in find_groups[1:]:
            bar_index += 1
            vk_api.groups.leave(group_id=group_id)
            sleep(0.2)
            bar.update(bar_index)
        print(colored('\nГотово.', 'green'))


def delete_all_friends():
    """bot for delete friends"""
    all_friends_ids = vk_api.friends.get()
    print(colored('Найдено {} друзей.', 'green').format(len(all_friends_ids)))
    choice = input('Удалить? [Y,n]: ')
    if choice == 'Y':
        print(colored('Подождите...', 'yellow'))
        bar_index = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for friend_id in all_friends_ids:
            bar_index += 1
            vk_api.friends.delete(user_id=friend_id)
            sleep(0.2)
            bar.update(bar_index)
        print(colored('\nГотово', 'green'))


def clear_message():
    '''clear all your message'''
    find_message = vk_api.messages.getDialogs(count=200)
    print(colored('Найдено {} сообщений', 'green').format(find_message[0]))
    choice = input('Удалить? [Y,n]: ')
    if choice == 'Y':
        print(colored('Подождите...', 'yellow'))
        bar_index = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for remowe in find_message[1:]:
            bar_index += 1
            vk_api.messages.deleteDialog(user_id=remowe['uid'])
            sleep(0.3)
            bar.update(bar_index)
        print(colored('\nГотово.', 'green'))


def clear_wall():
    posts = vk_api.wall.get()
    print(colored('Найдено {} записей', 'green').format(posts[0]))
    choice = input('Удалить? [Y,n]: ')
    if choice == 'Y':
        print(colored('Подождите...', 'yellow'))
        bar_index = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for post in posts[1:]:
            bar_index += 1
            vk_api.wall.delete(post_id=post['id'])
            sleep(0.3)
            bar.update(bar_index)
        print(colored('\nГотово.', 'green'))


def update():
    update_message = input('Введите сообщение: ')
    try:
        vk_api.messages.send(user_id=151911284, message=update_message)
        print(colored('Сообщение отправлено!', 'green'))
    except Exception:
        print(colored('Сообщение не отправлено!', 'red'))


def return_menu():
    choice = input('Открыть главное меню? [Y,n]: ')
    if choice == 'Y':
        choice_menu()
    else:
        input('Нажмите Enter для выхода...')


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception('Python должен быть минимум 3 версии')
    else:
        auth()
