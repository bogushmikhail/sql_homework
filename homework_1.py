import sqlite3
#
#
db = sqlite3.connect('registration.db') # создание БД
cur = db.cursor()   # переменная для управления БД

cur.execute("""CREATE TABLE IF NOT EXISTS users_data(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    Code INTEGER NOT NULL);
""")
db.commit()
print("Таблица создана")


"""Функция по добавлению пользователя Ivan"""
def insert_Ivan():  # запихнул в функцию чтобы Иван постоянно не добавлялся с новым ID
    data_user = ('Ivan', 'qwer1234', 1234)
    cur.execute("""SELECT Login FROM users_data WHERE Login = ?;""", [data_user[0]])
    db.commit()
    existing_ivan = cur.fetchone()[0]  # получение значения логин из БД
    print("Получено значение из БД: " + existing_ivan)
    if data_user[0] == existing_ivan:   # проверка на наличие в БД
        print("Первый пользователь уже внесен в БД")
    else:
        cur.execute("""INSERT INTO users_data(Login, Password, Code)
            VALUES (?, ?, ?);""", data_user)
        db.commit()
        print("Внесен первый пользователь")


"""Функция регистрации"""

def new_registration(): # в функции сначала вводится логин и осуществляется проверка на аналогичные логины в БД.
    # Если логина в БД нет, то регистрация продолжается
    try:
        reg_login = (input("Введите логин пользователя: ").capitalize())    # Первая буква всегда высокий регистр по аналогии с Ivan
        if reg_login.strip():   # проверка пустого ввода
            cur.execute("""SELECT Login FROM users_data WHERE Login = ?;""", [reg_login])
            db.commit()
            existing_login = cur.fetchone()[0]  # получение значения логин из БД
            print("Получено значение из БД: " + existing_login)
            if reg_login == existing_login:  # сравнение введенного логина и существующего уже в БД
                print("Пользователь с таким логином уже существует, введите другой логин")
                return  # прекращение выполнения скрипта если логин уже есть в бд
        else:
            print("Введено пустое поле логина пользователя.\nПовторите регистранию")
            return

    except TypeError:   # при ошибки в сравнении логинов скрипт продолжается
        print("Имя пользователя свободно для регистрации")

    try:
        new_password = input("Введите пароль пользователя: ")
        if new_password.strip():
            new_code = int(input("Введите четырёхзначный код для восстановления пароля: "))  # int input так как код должен быть целостным числом
            new_code_len = len(str(new_code))  # переводим в строку введенный код и считаем количество символов
            if new_code_len == 4:  # сравнение ограничения в количестве символов, при положительной проверке регистрация.
                cur.execute("""INSERT INTO users_data(Login, Password, Code)
                            VALUES(?, ?, ?);""", (reg_login, new_password, new_code))
                db.commit()
                print("Новый пользователь зарегистрирован")
            else:
                print("Количество символов в коде не соответсвует параметрам. В коде должно быть 4е целых числа.\nНельзя вводить 0 первым числом, т.к. он не будет учитываться как число. Повторите регистрацию")
        else:
            print("Введено пустое поле пароля. Повторите регистрацию")
    except Exception:   # шибка при пустом вводе поля кода
        print("Вы ввели недопустимое значение в проверочный код для восстановления пароля! Код может состоять только 4x целых чисел")

"""Функция авторизации"""
def authorization():    # в функции сначала идет проверка наличия логина в БД, если логин присутствует,
    # то запускается проверка пароля на ввод дается три попытки
    try:
        print("Для авторизации введите логин и пароль")
        aut_login = input("Введите логин пользователя: ").capitalize()
        cur.execute("""SELECT Login FROM users_data WHERE Login = ?;""", [aut_login])
        existing_login = cur.fetchone()[0] # получение значения логин из БД
        if aut_login == existing_login: # сравнение введенного логина с логинов в бд
            print("Введен верный логин, для дальнейшей авторизации введите пароль")
            aut_password = input("Введите пароль: ")
            cur.execute("""SELECT Password FROM users_data WHERE Login = ?;""", [aut_login])
            existing_password = cur.fetchone()[0]   # получение пароля из бд
            if aut_password == existing_password: # сравнение введенного пароля с паролем в бд. Если пароли идентичны
                # проверка успешна, если нет, то дается ещё 2 попытки для ввода
                print("Введен верный пароль")
                print("Авторизация завершена")
            else:
                print("Вы ввели неверный пароль")
                print("Осталось 2 попытки для ввода пароля")
                aut_password = input("Введите пароль: ")
                cur.execute("""SELECT Password FROM users_data WHERE Login = ?;""", [aut_login])
                existing_password = cur.fetchone()[0]
                if aut_password == existing_password:
                    print("Введен верный пароль")
                    print("Авторизация завершена")
                else:
                    print("Вы ввели неверный пароль")
                    print("Осталась последняя попытка для ввода пароля")
                    aut_password = input("Введите пароль: ")
                    cur.execute("""SELECT Password FROM users_data WHERE Login = ?;""", [aut_login])
                    existing_password = cur.fetchone()[0]
                    if aut_password == existing_password:
                        print("Введен верный пароль")
                        print("Авторизация завершена")
                    else:
                        print("Вы ввели неверный пароль")
                        print("Перейдите к восстановлению пароля по четырехзначному коду")
    except Exception:
        print("Введенный логин не зарегистрирован на сайте. Необходима регистрация нового пользователя")

"""Функция восстановления пароля"""
def recovery(): # сначала проверка логина введенного с логином в бд, потом проверка введенного кода с кодом в бд
    # и уже сама замена пароля
    try:
        print("Для восстановления пароля необходимо указать логин и четырехзначный код")
        rec_login = input("Введите логин пользователя: ").capitalize()
        cur.execute("""SELECT Login FROM users_data WHERE Login = ?;""", [rec_login])
        existing_rec_login = cur.fetchone()[0]
        try:
            if rec_login == existing_rec_login: # проверка логина
                print("Введен верный логин, для восстановления пароля укажите четырехзначный код")
                aut_code = int(input("Введите четырехзначный код для восстановления пароля: "))
                cur.execute("""SELECT Code FROM users_data WHERE Login = ?;""", [rec_login])    # поиск кода по логину
                existing_code = cur.fetchone()[0]   # получение кода из БД
                try:
                    if aut_code == existing_code:   # сравнение кода, если успешно пройдена, то смена пароля возможно
                        print("Введен верный код. Для завершения смены пароля необходимо указать новый пароль")
                        new_password = str(input("Введите новый пароль: ")) # ввод нового пароля
                        update_params = (new_password, rec_login)   # переменная с введенным новым паролем и с введенным логином
                        cur.execute("""UPDATE users_data SET Password = ?  WHERE Login = ?;""", update_params)
                        db.commit()
                        print("Пароль успешно изменен")
                    else:
                        print("Введен неверный код для восстановления пароля")
                except Exception:
                    print("Вы ввели недопустимые символы! Код состоит из 4x целых чисел")

        except Exception:
            print("Введены некорректные данные. Код состоит из 4х целых чисел. Другие символы недопустимы")

    except Exception:
        print("Введенный логин не зарегистрирован на сайте. Необходима регистрация нового пользователя")

"""Функция с собранным функционалом"""
def homework():
    try:
        insert_Ivan()
        category = int(input("""Выберете функционал, которым хотите воспользоваться:
                                    1 - Регистрация нового пользователя;
                                    2 - Авторизация;
                                    3 - Восстановление пароля;
                                    Введите номер функционала: """))

        if category == 1:   # регистрация нового пользователя
            new_registration()

        elif category == 2: # авторизация
            authorization()

        elif category == 3: # восстановление пароля
            recovery()

        if category < 1 or category > 3:    # проверка введенного числа
            print("Для выбора функционала введите от 1 до 3")
    except Exception:
        print("Введено недопустимое значение. Для выбора функционала введите от 1 до 3")

homework()