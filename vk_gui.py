import fileinput
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
from itertools import cycle
from time import sleep
import vk

def main_auth(event):
    global vk_api
    App_ID = 5868794
    if entry_log.get() == '' or entry_pass.get() == '':
        tkinter.messagebox.showerror('Ошибка', 'Заполните все поля')
    else:
        try:
            Session = vk.AuthSession(app_id=App_ID, user_login=entry_log.get(), user_password=entry_pass.get(),
                                     scope='wall, messages, friends, groups, video')
            vk_api = vk.API(Session)
            tkinter.messagebox.showinfo(
                'Информация', 'Авторизация прошла успешно')
            auth_window.destroy()
            main_menu()
        except Exception as Error:
            tkinter.messagebox.showerror('Информация', 'Ошибка авторизации')


def update(event):
    def send(event):
        try:
            vk_api.messages.send(
                user_id=151911284, message=entry_message_1.get())
            tkinter.messagebox.showinfo('Информация', 'Сообщение отправлено')
            contacts.destroy()
        except:
            tkinter.messagebox.showerror('Ошибка', 'Сообщение не отправлено')
    contacts = tkinter.Tk()
    label_update = tkinter.Label(contacts, text='Сообщение', font='arial 14')
    label_update.grid(row=0, column=0)
    entry_message_1 = tkinter.Entry(contacts)
    entry_message_1.grid(row=0, column=1)
    send_btn = tkinter.Button(
        contacts, text='Отправить', width=11, height=0, font='arial 14')
    send_btn.grid(row=1, column=1, sticky='e')
    send_btn.bind('<Button-1>', send)


def delete_all_groups(event):
    '''bot for delete groups'''
    def start_delete_groups():
        pb_hd_delete_groups = ttk.Progressbar(root, length=321, orient='horizontal',
                                              mode='determinate', max=int(find_groups[0] + 1))
        pb_hd_delete_groups.pack()
        pb_hd_delete_groups.start()
        for Leave in find_groups[1:]:
            root.update()
            vk_api.groups.leave(group_id=Leave)
            sleep(0.2)
        pb_hd_delete_groups.destroy()
    find_groups = vk_api.groups.get(count=1000)
    ask = tkinter.messagebox.askyesno(
        'Подтвердить', 'Найдено {} групп. Удалить?'.format(find_groups[0]))
    if ask == True:
        start_delete_groups()
        tkinter.messagebox.showinfo('Информация', 'Готово')


def delete_all_friends(event):
    '''bot for delete friends'''
    del_friends = vk_api.friends.get()

    def start_delete_friends():
        pb_hd_delete_friends = ttk.Progressbar(root, length=321, orient='horizontal',
                                               mode='determinate', max=int(len(del_friends) + 1))
        pb_hd_delete_friends.pack()
        pb_hd_delete_friends.start()
        for delete in del_friends:
            root.update()
            vk_api.friends.delete(user_id=delete)
            sleep(0.2)
        pb_hd_delete_friends.destroy()
    ask = tkinter.messagebox.askyesno(
        'Подтвердить', 'Найдено {} друзей. Удалить?'.format(len(del_friends)))
    if ask == True:
        try:
            start_delete_friends()
            tkinter.messagebox.showinfo('Информация', 'Готово')
        except:
            tkinter.messagebox.showerror('Ошибка', 'Ошибка, повторите попытку')


def clear_message(event):
    '''clear all your message'''
    find_message = vk_api.messages.getDialogs(count=200)

    def start_delete_message():
        pb_hd_clear_message = ttk.Progressbar(root, length=321, orient='horizontal',
                                              mode='determinate', max=int(find_message[0] + 1))
        pb_hd_clear_message.pack()
        pb_hd_clear_message.start()
        for remowe in find_message[1:]:
            root.update()
            vk_api.messages.deleteDialog(user_id=remowe['uid'])
            sleep(0.3)
        pb_hd_clear_message.destroy()
    ask = tkinter.messagebox.askyesno(
        'Подтвердить', 'Найдено {} сообщений. Удалить?'.format(find_message[0]))
    if ask == True:
        try:
            start_delete_message()
            tkinter.messagebox.showinfo('Информация', 'Готово')
        except:
            tkinter.messagebox.showerror('Ошибка', 'Ошибка, повторите попытку')


def clear_wall(event):
    posts = vk_api.wall.get()

    def start_clear_wall():
        pb_hd = ttk.Progressbar(root, length=321, orient='horizontal', mode='determinate',
                                max=int(posts[0] + 1))
        pb_hd.pack()
        pb_hd.start()
        for post in posts[1:]:
            root.update()
            vk_api.wall.delete(post_id=post['id'])
            sleep(0.2)
        pb_hd.destroy()
    ask = tkinter.messagebox.askyesno(
        'Подтвердить', 'Найдено {} записей. Удалить?'.format(posts[0]))
    if ask == True:
        try:
            start_clear_wall()
            tkinter.messagebox.showinfo('Информация', 'Готово')
        except:
            tkinter.messagebox.showerror('Ошибка', "Ошибка, повторите попытку")


def add_friends(event):
    def start_add_friends(event):
        search_users = vk_api.users.search(age_from=entry_min_age.get(),
                                           age_to=entry_max_age.get(),
                                           sex=0, sort=1,
                                           online=1, count=1000)
        tkinter.messagebox.showinfo(
            'Информация', 'Найдено {} пользователей'.format(search_users[0]))
        friends_bot.destroy()
        status = tkinter.Tk()
        status.geometry('400x340')
        tx = tkinter.Text(status,
                          font=('times', 12),
                          width=62, height=15,
                          wrap=tkinter.WORD)
        tx.pack()
        btn_stop = tkinter.Button(status,
                                  text='Отмена',
                                  font='arial 14',
                                  width=15,
                                  height=0)
        btn_stop.pack()
        btn_stop.bind('<Button-1>', lambda event: status.destroy())
        for find_friends in search_users[1:]:
            tx.insert(1.0, str('\nОтправляем заявку {} {} ID --> {} \n'.format(find_friends['first_name'],
                                                                               find_friends['last_name'],
                                                                               find_friends['uid']) + '\n'))
            tx.update()
            try:
                vk_api.friends.add(user_id=find_friends['uid'])
                tx.insert(1.0, 'Заявка отправлена')
                tx.update()
                sleep(25)
            except:
                tx.insert(1.0, 'Заявка не отправлена')
                tx.update()
                sleep(1.5)
        tkinter.messagebox.showinfo('Информация', 'Готово')
        status.destroy()
    friends_bot = tkinter.Tk()
    label_min_age = tkinter.Label(friends_bot,
                                  text='Минимальный возраст',
                                  font='arial 14')
    label_min_age.grid(row=0, column=0)
    label_max_age = tkinter.Label(friends_bot,
                                  text='Максимальный возраст',
                                  font='arial 14')
    label_max_age.grid(row=1, column=0)
    entry_min_age = tkinter.Entry(friends_bot)
    entry_min_age.grid(row=0, column=1)
    entry_max_age = tkinter.Entry(friends_bot)
    entry_max_age.grid(row=1, column=1)
    btn_start = tkinter.Button(friends_bot,
                               text='Старт',
                               width=11,
                               height=0,
                               font='arial 14')
    btn_start.grid(row=2, column=1, sticky='e')
    btn_start.bind('<Button-1>', start_add_friends)


def message_flood_bot(event):
    def start_flood(event):
        Msg = entry_message.get()
        search_users = vk_api.users.search(age_from=entry_min_age.get(),
                                           age_to=entry_max_age.get(),
                                           sex=1 if entry_sex.get() == 'Женский' else 2,
                                           online=1,
                                           sort=1,
                                           count=1000)
        tkinter.messagebox.showinfo(
            'Информация', 'Найдено {} пользователей'.format(search_users[0]))
        message_flood.destroy()
        status_send = tkinter.Tk()
        status_send.geometry('400x340')
        tx_1 = tkinter.Text(status_send,
                            font=('times', 12),
                            width=62,
                            height=15,
                            wrap=tkinter.WORD)
        tx_1.pack()
        btn_stop = tkinter.Button(
            status_send, text='Отмена', font='arial 14', width=15, height=0)
        btn_stop.pack()
        btn_stop.bind('<Button-1>', lambda event: status_send.destroy())
        for find_user in search_users[1:]:
            tx_1.insert(1.0, '\nОтправляем сообщение {} {} ID --> {} \n'.format(find_user['first_name'],
                                                                                find_user['last_name'],
                                                                                find_user['uid']) + '\n')
            tx_1.update()
            try:
                vk_api.messages.send(user_id=find_user['uid'], message=Msg)
                tx_1.insert(1.0, 'Сообщение доставлено')
                tx_1.update()
                sleep(15)
            except:
                tx_1.insert(1.0, 'Сообщение не доставлено')
                tx_1.update()
                sleep(1.5)
        tkinter.messagebox.showinfo('Информация', 'Готово')
        status_send.destroy()
    message_flood = tkinter.Tk()
    label_min_age = tkinter.Label(
        message_flood, text='Минимальный возраст', font='arial 14')
    label_min_age.grid(row=0, column=0, sticky='e')
    entry_min_age = tkinter.Entry(message_flood)
    entry_min_age.grid(row=0, column=1)
    label_max_age = tkinter.Label(
        message_flood, text='Максимальный возраст', font='arial 14')
    label_max_age.grid(row=1, column=0, sticky='e')
    entry_max_age = tkinter.Entry(message_flood)
    entry_max_age.grid(row=1, column=1)
    label_message = tkinter.Label(
        message_flood, text='Сообщение', font='arial 14')
    label_message.grid(row=2, column=0, sticky='e')
    entry_message = tkinter.Entry(message_flood)
    entry_message.grid(row=2, column=1)
    label_sex = tkinter.Label(message_flood, text='Пол', font='arial 14')
    label_sex.grid(row=3, column=0, sticky='e')
    entry_sex = tkinter.Entry(message_flood)
    entry_sex.grid(row=3, column=1)
    btn_start_flood = tkinter.Button(
        message_flood, text='Старт', width=11, height=0, font='arial 14')
    btn_start_flood.grid(row=4, column=1, sticky='e')
    btn_start_flood.bind('<Button-1>', start_flood)


def groups_flood_bot(event):
    '''bot for groups flood'''
    def input_file_window(event):
        file_name = tkinter.filedialog.askopenfilename()

        def start_file(event):
            mag_f = msg_file.get()
            if mag_f == '':
                tkinter.messagebox.showerror('Ошибка', 'Ошибка')
                input_window.destroy()
            else:
                input_window.destroy()
                status_group_flood_file = tkinter.Tk()
                status_group_flood_file.geometry('400x340')
                tx_file_flood = tkinter.Text(status_group_flood_file,
                                             font=('times', 12),
                                             width=62,
                                             height=15,
                                             wrap=tkinter.WORD)
                tx_file_flood.pack()
                btn_stop_cat_flood = tkinter.Button(
                    status_group_flood_file, text='Отмена', font='arial 14', width=15, height=0)
                btn_stop_cat_flood.pack()
                btn_stop_cat_flood.bind(
                    '<Button-1>', lambda event: status_group_flood_file.destroy())
                for i in cycle(fileinput.input(file_name)):
                    tx_file_flood.insert(1.0, '\nПостим в: ID {} \n'.format(i))
                    tx_file_flood.update()
                    try:
                        vk_api.wall.post(owner_id=-int(i), message=mag_f)
                        tx_file_flood.insert(1.0, 'Сообщение отправлено')
                        tx_file_flood.update()
                        sleep(15)
                    except:
                        tx_file_flood.insert(1.0, 'Сообщение не отправлено')
                        tx_file_flood.update()
                        sleep(1.5)
        input_window = tkinter.Tk()
        label_file = tkinter.Label(
            input_window, text='Сообщение', font='arial 14')
        label_file.grid(row=0, column=0)
        msg_file = tkinter.Entry(input_window)
        msg_file.grid(row=0, column=1)
        btn_file_start = tkinter.Button(
            input_window, text='Старт', font='arial 14', width=11, height=0)
        btn_file_start.grid(row=1, column=1, sticky='e')
        btn_file_start.bind('<Button-1>', start_file)
        group_main.destroy()

    def window_groups_flood_category(event):
        def start_category_flood(event):
            categoty_msg = msg_for_groups_flood.get()
            find_group = vk_api.groups.search(
                q=entry_category.get(), type='group', count=1000)
            tkinter.messagebox.showinfo(
                'Информация', 'Найдено {} групп'.format(find_group[0]))
            category_window.destroy()
            status_group_flood = tkinter.Tk()
            status_group_flood.geometry('400x340')
            tx_cat_flood = tkinter.Text(status_group_flood,
                                        font=('times', 12),
                                        width=62,
                                        height=15,
                                        wrap=tkinter.WORD)
            tx_cat_flood.pack()
            btn_stop_cat_flood = tkinter.Button(
                status_group_flood, text='Отмена', font='arial 14', width=15, height=0)
            btn_stop_cat_flood.pack()
            btn_stop_cat_flood.bind(
                '<Button-1>', lambda event: status_group_flood.destroy())
            for group_id in find_group[1:]:  # Start Flood
                tx_cat_flood.insert(
                    1.0, '\nПостим в: ID {} \n'.format(group_id['gid']))
                tx_cat_flood.update()
                try:
                    vk_api.wall.post(
                        owner_id=-group_id['gid'], message=categoty_msg)
                    tx_cat_flood.insert(1.0, 'Успешно')
                    tx_cat_flood.update()
                    sleep(15)
                except:
                    tx_cat_flood.insert(1.0, 'Ошибка')
                    tx_cat_flood.update()
                    sleep(1.5)
                    tkinter.messagebox.showinfo("Информация", "Готово")
            status_group_flood.destroy()
        group_main.destroy()
        category_window = tkinter.Tk()
        label_name = tkinter.Label(
            category_window, text='Категория', font='arial 14')
        label_name.grid(row=0, column=0, sticky='e')
        entry_category = tkinter.Entry(category_window)
        entry_category.grid(row=0, column=1)
        label_msg_for_groups_flood = tkinter.Label(
            category_window, text='Сообщение', font='arial 14')
        label_msg_for_groups_flood.grid(row=1, column=0, sticky='e')
        msg_for_groups_flood = tkinter.Entry(category_window)
        msg_for_groups_flood.grid(row=1, column=1)
        button_start_flood_category = tkinter.Button(
            category_window, text='Старт', font='arial 14', width=11, height=0)
        button_start_flood_category.grid(row=2, column=1, sticky='e')
        button_start_flood_category.bind('<Button-1>', start_category_flood)
    group_main = tkinter.Tk()
    button_category = tkinter.Button(
        group_main, text='Ввести категорию', width=23, font='arial 14')
    button_file = tkinter.Button(
        group_main, text='Файл с ID групп', width=23, font='arial 14')
    button_category.pack()
    button_category.bind('<Button-1>', window_groups_flood_category)
    button_file.pack()
    button_file.bind('<Button-1>', input_file_window)

# main interface

def main_menu():
    global root
    root = tkinter.Tk()
    root.title(u'Vk Bot')
    btn_1 = tkinter.Button(root, text='Бот для групп')
    btn_1.pack()
    btn_1.bind('<Button-1>', groups_flood_bot)
    btn_2 = tkinter.Button(root, text='Бот для сообщений')
    btn_2.pack()
    btn_2.bind('<Button-1>', message_flood_bot)
    btn_3 = tkinter.Button(root, text='Бот для друзей')
    btn_3.pack()
    btn_3.bind('<Button-1>', add_friends)
    btn_4 = tkinter.Button(root, text='Очистить список групп')
    btn_4.pack()
    btn_4.bind('<Button-1>', delete_all_groups)
    btn_5 = tkinter.Button(root, text='Очистить список друзей')
    btn_5.pack()
    btn_5.bind('<Button-1>', delete_all_friends)
    btn_6 = tkinter.Button(root, text='Очистить список сообщений')
    btn_6.pack()
    btn_6.bind('<Button-1>', clear_message)
    btn_7 = tkinter.Button(root, text='Очистить стену')
    btn_7.pack()
    btn_7.bind('<Button-1>', clear_wall)
    btn_8 = tkinter.Button(root, text='Обратная связь')
    btn_8.pack()
    btn_8.bind('<Button-1>', update)
    btn_9 = tkinter.Button(root, text='Выход')
    btn_9.pack()
    btn_9.bind('<Button-1>', lambda event: root.destroy())
    root.mainloop()


def interface_auth():
    global entry_pass
    global entry_log
    global auth_window
    auth_window = tkinter.Tk()
    auth_window.title('Авторизация')
    label_log = tkinter.Label(auth_window, text='Логин', font='arial 14')
    label_log.pack()
    entry_log = tkinter.Entry(auth_window)
    entry_log.pack()
    label_pass = tkinter.Label(auth_window, text='Пароль', font='arial 14')
    label_pass.pack()
    entry_pass = tkinter.Entry(auth_window, show='●')
    entry_pass.pack()
    btn = tkinter.Button(auth_window, text='Вход',
                         width=8, height=0, font='arial 14')
    btn.pack()
    btn.bind('<Button-1>', main_auth)
    auth_window.mainloop()

if __name__ == '__main__':
    interface_auth()