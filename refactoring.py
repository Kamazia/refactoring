import hashlib
import json
import os
import re
import uuid
from tkinter import messagebox
from typing import Any
REGEX_LOGIN = r"^([a-zA-Z][a-zA-Z\d_]{2,12})"
REGEX_PASSWORD = r"^([^\\/\s]{5,12})$"


def check_user_data_file(path):
    if not os.path.exists(path):
        with open(path,'w') as file:
            json.dump({},file,indent = 4)

    return path


class Authentication:
    def __init__(self,entry_login,entry_password,checkbox,window) -> None:
        self.login = entry_login.get()
        self.password = entry_password.get()
        self.entry_login = entry_login
        self.entry_password = entry_password
        self.checkbox = checkbox
        self.window = window
        self.path = check_user_data_file(f'{os.getcwd()}\\data\\users_data.json')

        self.login_or_registration()

    def __clear_fields(self) -> None:
        self.entry_login.delete(0,'end')
        self.entry_password.delete(0,'end')

    def __check_password(self,hashed_password, salt, user_password) -> Any:
        return hashed_password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    def __hash_password(self,password) -> tuple[str,str]:
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest(),salt

    def login_or_registration(self):
        if re.fullmatch(REGEX_LOGIN, self.login) != None and re.fullmatch(REGEX_PASSWORD, self.password) != None:

            with open(self.path,'r') as file: # Читаем весь json файл с данными
                data_from_file:dict = json.load(file)

            if self.checkbox:
                if data_from_file.get(self.login):
                    messagebox.showinfo(title = None, message = 'Пользователь с таким именем уже существует', parent = self.window)

                else:
                    hashed_password,salt = self.__hash_password(self.password)

                    with open(self.path,'w') as file:
                        data_from_file.update([(self.login,{'Password':hashed_password,'Salt':salt})])
                        json.dump(data_from_file,file,indent = 4)

                    messagebox.showinfo(title = None, message = 'Пользователь сохранён\n\nВведите данные для входа повторно', parent = self.window)
                    self.__clear_fields()

            else:
                if not data_from_file.get(self.login):
                    messagebox.showinfo(title = None, message = 'Данный пользователь не зарегистрирован', parent = self.window)

                else:
                    if self.__check_password(data_from_file[self.login]['Password'], data_from_file[self.login]['Salt'],self.password):
                        self.window.destroy()

                    else:
                        messagebox.showinfo(title = None, message = 'Введен не верный пароль', parent = self.window)
                        self.entry_password.delete(0,'end')

        else:
            info = 'Введены не корректные login или password\n\n* Допустимы только латинские буквы\n* НЕ допустимы символы: \ /, пробел \n* login - должен быть 2 - 12 символов и начинаться с буквы\n* password - пароль должен быть 5 - 12 символов'
            messagebox.showinfo(title = None, message = info, parent = self.window)
            self.__clear_fields()