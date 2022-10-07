import hashlib
import json
import os
import re
import uuid
from tkinter import messagebox


class Authentication:
    def __init__(self,entry_login,entry_password,checkbox,window) -> None:
        self.login = entry_login.get()
        self.password = entry_password.get()
        self.entry_login = entry_login
        self.entry_password = entry_password
        self.checkbox = checkbox
        self.window = window
        self.path = f'{os.getcwd()}\\data\\users_data.json' 

        self.log()

    def __check_password(self,hashed_password, salt, user_password):
        return hashed_password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    def __hash_password(self,password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest(),salt

    def log(self):
        regex_login = r"^([a-zA-Z][a-zA-Z\d_]{2,12})"
        regex_pass = r"^([^\\/\s]{5,12})$"

        if re.fullmatch(regex_login, self.login) != None and re.fullmatch(regex_pass, self.password) != None: # Проверка введенных данных на валидность
            if self.checkbox == True: # Если это регистрация
                print('ok, data valid')
                hashed_password,salt = self.__hash_password(self.password)
                try: # Имя пользователя имеется в базе
                    with open(self.path,'r') as file: # Читаем весь json и помещаем в a
                        a = json.load(file)
                        print(a[self.login])
                        messagebox.showinfo(title = None, message = 'Пользователь с таким именем уже существует', parent = self.window)

                except KeyError: # Имя пользователя НЕ имеется в базе
                    with open(self.path,'r') as file:
                        a = json.load(file)
                        print(a)

                    with open(self.path,'w') as file:
                        a [self.login] = {'Password':hashed_password,'Salt':salt}
                        print(a)

                        json.dump(a,file,indent = 4)

                    messagebox.showinfo(title = None, message = 'Пользователь сохранён\n\nВведите данные для входа повторно', parent = self.window)
                    self.entry_login.delete(0,'end')
                    self.entry_password.delete(0,'end')

                except json.decoder.JSONDecodeError: # Файл пуст, добавление первой записи
                    with open(self.path,'w') as file:
                        a = {}
                        a [self.login] = {'Password':hashed_password,'Salt':salt}
                        print(a)

                        json.dump(a,file,indent = 4)

                        messagebox.showinfo(title = None, message = 'Пользователь сохранён\n\nВведите данные для входа повторно', parent = self.window)
                        self.entry_login.delete(0,'end')
                        self.entry_password.delete(0,'end')

                except FileNotFoundError:
                    messagebox.showinfo(title = None, message = 'Файл с данными отсутствует.\nСоздан новый файл с данными', parent = self.window)
                    with open(self.path,'w') as file:
                        a = {}
                        a [self.login] = {'Password':hashed_password,'Salt':salt}
                        print(a)

                        json.dump(a,file,indent = 4)

                        messagebox.showinfo(title = None, message = 'Пользователь сохранён\n\nВведите данные для входа повторно', parent = self.window)
                        self.entry_login.delete(0,'end')
                        self.entry_password.delete(0,'end')

            else: # Если это не регистрация
                try:
                    with open(self.path,'r') as file: # Читаем весь json и помещаем в a
                        a = json.load(file)
                        print(a[self.login])

                        if self.__check_password(a[self.login]['Password'],a[self.login]['Salt'],self.password):
                            self.window.destroy()
                            
                        else:
                            messagebox.showinfo(title = None, message = 'Введен не верный пароль', parent = self.window)
                            self.entry_password.delete(0,'end')

                except FileNotFoundError:
                    messagebox.showinfo(title = None, message = 'Файл с данными не найден или отсутствует', parent = self.window)

                except json.decoder.JSONDecodeError:
                    messagebox.showinfo(title = None, message = 'Файл с данными пуст', parent = self.window)
                
                except KeyError:
                    messagebox.showinfo(title = None, message = 'Данный пользователь не зарегистрирован', parent = self.window)

        else: # Если данные не валидны
            info = 'Введены не корректные login или password\n\n* Допустимы только латинские буквы\n* НЕ допустимы символы: \ /, пробел \n* login - должен быть 2 - 12 символов и начинаться с буквы\n* password - пароль должен быть 5 - 12 символов'
            messagebox.showinfo(title = None, message = info, parent = self.window)
            self.entry_login.delete(0,'end')
            self.entry_password.delete(0,'end')