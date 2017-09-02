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


def Authorization():
    """login vk"""
    global vk_api
    try:
        print('''1. Использовать своё приложение
2. Использовать стандартное приложение''')
        try:
            app =int(input('Ваш выбор: '))
            if app == 1:
                input_id = int(input('App ID: '))
                App_ID = input_id
            elif app == 2:
                App_ID = 5868794
            else:
                print(Error)
        except Exception as Error:
            print(colored('Ошибка', 'red'))
            Authorization()
        Login_VK = input('Введите ваш логин: ')
        Password_VK = getpass('Введите ваш пароль: ')
        try:
            Session = vk.AuthSession(app_id=App_ID, user_login=Login_VK, user_password=Password_VK,
                                     scope='wall, messages, friends, groups, video')
            vk_api = vk.API(Session)
            print(colored('Авторизация прошла успешно', 'green'))
            choice_menu()
        except:
            print(colored('Ошибка авторизации', 'red'))
            Authorization()
    except:
        exit = input('Нажмите Enter для выхода...')
        pass
def choice_menu():
    '''nenu'''
    print(colored('''1. Бот для груп
2. Бот для сообщений
3. Бот для друзей
4. Очистить список групп
5. Очистить список друзей
6. Очистить список сообщений
7. Очистить стену
8. Выход
9. Обратная связь''', 'yellow'))
    try:
        Choice = int(input('Ваш выбор: '))
        if Choice == 1:
            groups_flood_bot()
            return_menu()
        elif Choice == 2:
            message_flood()
            return_menu()
        elif Choice == 3:
            add_friends()
            return_menu()
        elif Choice == 4:
            delete_all_groups()
            return_menu()
        elif Choice == 5:
            delete_all_friends()
            return_menu()
        elif Choice == 6:
            clear_message()
            return_menu()
        elif Choice == 7:
            clear_wall()
            return_menu()
        elif Choice == 8:
            exit = input('Нажмите Enter для выхода...')
        elif Choice == 9:
            update()
            return_menu()
        else:
            print(NotFOund)
    except Exception as NotFound:
        print(colored('Опция не найдена или сессия оборвана', 'red'))
        print('''1. Пройти авторизацию заново
2. Открыть главное меню''')
        exception = int(input('Ваш выбор: '))
        if exception == 1:
            Authorization()
        elif exception == 2:
            choice_menu()
def groups_flood_bot():
    '''bot for groups flood'''
    init()
    Select = int(input('1 - Искать группы по категориям, 2 - Список групп из файла: '))
    if Select == 1:
        category = input('Введите категорию: ')
        find_group = vk_api.groups.search(q=category, type='group', count=1000)
        print(colored('Найдено {} групп'.format(find_group[0]), 'green'))
        message_for_flood = input('Введите сообщение: ')
        set_time = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))
        for group_id in find_group[1:]: # Start Flood
            try:
                print('Постим в: ID ', group_id['gid'])
                vk_api.wall.post(owner_id=-group_id['gid'], message=message_for_flood)
                for progres in progress.bar(range(set_time)):
                    sleep(1)
                print(colored('Сообщение доставлено.', 'green'))
            except Exception:
                print(colored('Сообщение не доставлено.', 'red'))
                sleep(0.3)
    elif Select == 2:
        Path_FIle = input('Файл: ')
        file = open(Path_FIle)
        Delay_time = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))
        Massege = input('Введите сообщение: ')
        for i in cycle(file):
            try:
                print('Постим в: ID {}'.format(i))
                vk_api.wall.post(owner_id=-int(i), message=Massege)
                for progres in progress.bar(range(Delay_time)):
                    sleep(1)
                print(colored('Сообщение доставлено', 'green'))
            except:
                print(colored('Сообщение не доставлено', 'red'))
                sleep(1)
def message_flood():
    '''bot for message flood'''
    Start_age = int(input('Минимальный возраст: '))
    End_age = int(input('Максимальный возраст: '))
    Sex = int(input('Пол [1 - Женский, 2 - Мужской, 0 - Любой]: '))
    Online = int(input('Онлайн [1 - искать только пользователей онлайн, 0 - любых]: '))
    Message = input('Введите сообщение: ')
    delay_time = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))
    search_users = vk_api.users.search(age_from=Start_age, age_to=End_age, sex=Sex,
                                       online=Online, sort=1, count=1000)
    print(colored('Найдено {} пользователей'.format(search_users[0]), 'green'))
    for find_user in search_users[1:]:
        try:
            print('Отправляем сообщение {} {} ID --> {}'.format(find_user['first_name'],
                                                                find_user['last_name'], find_user['uid']))
            vk_api.messages.send(user_id=find_user['uid'], message=Message)
            for Status in progress.bar(range(delay_time)):
                sleep(1)
            print(colored('Сообщение доставлено', 'green'))
        except:
            print(colored('Сообщение не доставлено', 'red'))
            sleep(0.3)
def add_friends():
    '''bot for add friends'''
    Min_age = int(input('Минимальный возраст: '))
    Max_age = int(input('Максимальный возраст: '))
    Sex = int(input('Пол [1 - Женский, 2 - Мужской, 0 - Любой]: '))
    Online = int(input('Онлайн [1 - искать пользователей онлайн, 0 - любых]: '))
    Delay_time = int(input('Укажите время задержки [Рекомендовано 15 - 20 секунд]: '))
    search_users = vk_api.users.search(age_from=Min_age, age_to=Max_age, sex=Sex, sort=1, online=Online, count=1000)
    for find_friends in search_users[1:]:
        try:
            print('Отправляем заявку {} {} ID --> {}'.format(find_friends['first_name'], find_friends['last_name'], find_friends['uid']))
            vk_api.friends.add(user_id=find_friends['uid'])
            for Status in progress.bar(range(Delay_time)):
                sleep(1)
            print(colored('Заявка отправлена', 'green'))
        except:
            print(colored('Заявка не отправлена', 'red'))
            sleep(0.3)
def delete_all_groups():
    '''bot for delete groups'''
    find_groups = vk_api.groups.get(count=1000)
    print(colored('Найдено {} групп', 'green').format(find_groups[0]))
    Choice = input('Старт? [Y,n]: ')
    if Choice == 'Y':
        print(colored('Подождите...', 'yellow'))
        bar_index = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for Leave in find_groups[1:]:
            bar_index += 1
            vk_api.groups.leave(group_id=Leave)
            sleep(0.2)
            bar.update(bar_index)
        print(colored('\nГотово.', 'green'))
    else:
        pass
def delete_all_friends():
    '''bot for delete friends'''
    del_friends = vk_api.friends.get()
    print(colored('Найдено {} друзей.', 'green').format(len(del_friends)))
    Question = input('Удалить? [Y,n]: ')
    if Question == 'Y':
        print(colored('Подождите...', 'yellow'))
        bar_index = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for delete in del_friends:
            bar_index += 1
            vk_api.friends.delete(user_id=delete)
            sleep(0.2)
            bar.update(bar_index)
        print(colored('\nГотово', 'green'))
    else:
        pass
def clear_message():
    '''clear all your message'''
    find_message = vk_api.messages.getDialogs(count=200)
    print(colored('Найдено {} сообщений', 'green').format(find_message[0]))
    d_message = input('Удалить? [Y,n]: ')
    if d_message == 'Y':
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
    delete_posts = input('Удалить? [Y,n]: ')
    if delete_posts == 'Y':    
        print(colored('Подождите...', 'yellow'))
        bar_index = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        for post in posts[1:]:
            bar_index += 1
            vk_api.wall.delete(post_id=post['id'])
            sleep(0.3)
            bar.update(bar_index)
        print(colored('\nГотово.', 'green'))
    else:
        pass
def update():
    upd_message = input('Введите сообщение: ')
    try:
        vk_api.messages.send(user_id=151911284, message=upd_message)
        print(colored('Сообщение отправлено!', 'green'))
    except:
        print(colored('Сообщение не отправлено!', 'red'))
def return_menu():
    Choice = input('Открыть главное меню? [Y,n]: ')
    if Choice == 'Y':
        choice_menu()
    else:
        input('Нажмите Enter для выхода...')
if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception('Python должен быть минимум 3 версии')
    else:
        Authorization()