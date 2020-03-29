from flask import Flask, jsonify, request, make_response, current_app
from cocktails_rating.helpers import does_record_exists
import sqlite3
import crypt
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = current_app


class Registration:
    def __init__(self, con):
        self.con = con('../db/authorization.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def new_user(self, login, password, email):
        if does_record_exists(self.cur, 'login', 'Users', ('login', login)):
            return {'Status: ': 'Failed', 'Description': 'User already exist, try other login'}
        else:
            hash = generate_password_hash(password)
            pass_data = (login, hash)
            profile = (login, email)
            self.add_to_db(profile, pass_data)
        return {'Status': 'Success'}

    def add_to_db(self, profile, password):
        self.cur.execute(''' 
                        INSERT INTO Users (login, email, created_at)
                        VALUES (?, ?, datetime("now"))
                        ''', profile)
        self.cur.execute(''' 
                        INSERT INTO Passwords (login, hash)
                        VALUES (?, ?)
                        ''', password)
        self.con.commit()
        return


class Log:
    def __init__(self, con):
        self.con = con('../db/authorization.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def get_hash_from_db(self, login):
        value = self.cur.execute(f'''
                        SELECT hash
                        FROM Passwords 
                        WHERE login = "{login}"
                        ''')
        hash= []
        for _ in value:
            hash.append(_[0])
        return hash

    def loginto(self):
        auth = request.authorization
        login = auth.username
        password = auth.password
        print(auth)
        print(password)
        print(login)
        if not does_record_exists(self.cur, 'login', 'Users', ('login', login)):
            return {'Status: ': 'Failed', 'Description: ': "User doesn't exsist."}

        elif check_password_hash(self.get_hash_from_db(login), password):
            token = jwt.encode(
                {'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},
                app['secret_key'])
            return {'Status: ': 'Success', 'Token': token.decode('UTH-8')}

        return {'Status: ': 'Failed', 'Description': 'Incorrect Password'}


class ForgotPassword:
    def __init__(self, con):
        self.con = con('../db/authorization.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def send_new_password(self, login, email):
        if does_record_exists(self.cur, '*', 'Users', ('login', login),( 'email', email)):
            new_password = self.generate_new_password()
            self.change_password(new_password, login)
            return {'Status: ': 'Success', 'Description: ':'Email with new password sended'}  # Dopisz wysyłanie maili z przypomnieniem
        else:
            return {'Status: ': 'Failed', 'Description': "User doesn't exist"}

    def change_password(self, new_password, login):
        hash = generate_password_hash(new_password)
        self.cur.execute(f'''
                        UPDATE Passwords
                        SET hash = "{hash}"
                        WHERE login = "{login}"
                        ''')
        self.con.commit()
        return

    def generate_new_password(self):
        return crypt.mksalt(crypt.METHOD_SHA512)