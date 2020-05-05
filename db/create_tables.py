# import sqlite3
# db_path = 'cocktails.db'
#
#
# # Create tables
# def create(cur):
#     # Pubs table
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS Pubs (
#         pub_id INTEGER PRIMARY KEY ASC,
#         pub_name VARCHAR NOT NULL);
#         """)
#
#     # Cocktails table
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS Cocktails (
#         cocktail_id INTEGER PRIMARY KEY ASC,
#         cocktail_name VARCHAR NOT NULL,
#         pub_id INTEGER NOT NULL,
#         FOREIGN KEY (pub_id) REFERENCES Pubs(pub_id));
#         ''')
#
#     # Ratings table
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS Ratings (
#         rating_id INTEGER PRIMARY KEY ASC,
#         cocktail_id INTEGER NOT NULL,
#         rating INTEGER,
#         FOREIGN KEY (cocktail_id) REFERENCES Cocktails(cocktail_id));
#         ''')
#
#     # Passwords table
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS Passwords (
#         pass_id INTEGER PRIMARY KEY ASC,
#         user_id INTEGER NOT NULL,
#         hash VARCHAR NOT NULL,
#         FOREIGN KEY (user_id) REFERENCES Users(user_id));
#         ''')
#
#     # Users Table
#     cur.execute('''
#         CREATE TABLE IF NOT EXISTS Users (
#         user_id INTEGER PRIMARY KEY ASC,
#         login VARCHAR NOT NULL,
#         email VARCHAR NOT NULL,
#         modified_on VARCHAR);
#         ''')
#     return True
#
#
# if __name__ == '__main__':
#     con = sqlite3.connect(db_path)
#     con.row_factory = sqlite3.Row
#     create(con.cursor())
#     con.commit()
from db.models import CocktailModel, PubModel
from flask import current_app

db = current_app.config['SQLALCHEMY_DATABASE_URI']

pubs_list = []
for i in range(1, 5):
    name = 'Pub' + str(i)
    pubs_list.append((None, name))

data = pubs_list
db.session.add(data)