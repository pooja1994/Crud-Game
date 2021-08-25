from flask import Flask, render_template, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import create_engine
import pandas as pd
import jwt
import datetime

key = "AQwerty781Q"
engine = create_engine('mysql://root:root@127.0.0.1:3308/game_database')

with open('C:/Users/charan/Downloads/games_data.csv', 'r') as file:
    data_df = pd.read_csv(file)
    try:
        data_df.to_sql('games', con=engine, index=True, index_label='id')
    except ValueError:
        pass

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3308/game_database'
db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = 'games'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(255), nullable=False)
    # nullable is false so the column can't be empty
    platform = db.Column(db.String(200), nullable=False)
    score = db.Column(db.String(10), nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    editors_choice = db.Column(db.String(1), nullable=False)

    def json(self):
        return {'id': self.id, 'title': self.title,
                'platform': self.platform, 'genre': self.genre, 'score': self.score,
                'editors_choice': self.editors_choice}

    @staticmethod
    def add_game(id, title, platform, genre, score, editors_choice):
        new_game = Game(id=id, title=title, platform=platform, genre=genre, score=score, editors_choice=editors_choice)
        db.session.add(new_game)
        db.session.commit()

    @staticmethod
    def get_all_games(genre, platform, score, editors_choice, sort):
        gamelist = Game.query

        if genre:
            gamelist = gamelist.filter_by(genre=genre)
        if platform:
            gamelist = gamelist.filter_by(platform=platform)
        if score:
            gamelist = gamelist.filter_by(score=score)
        if editors_choice:
            gamelist = gamelist.filter_by(editors_choice=editors_choice)
        if sort and sort == 'true':
            gamelist = gamelist.order_by(Game.score)

        return [Game.json(games) for games in gamelist.all()]

    @staticmethod
    def get_game(title):
        return [Game.json(Game.query.filter_by(title=title).first())]

    @staticmethod
    def update_game(game_id, title, platform, genre, score, editors_choice):
        game_to_update = Game.query.filter_by(id=game_id).first()
        game_to_update.title = title
        game_to_update.platform = platform
        game_to_update.genre = genre
        game_to_update.score = score
        game_to_update.editors_choice = editors_choice
        db.session.commit()

    @staticmethod
    def delete_game(id):
        Game.query.filter_by(id=id).delete()
        db.session.commit()

    if __name__ == "__main__()":
        app.debug = True
        app.run()


class User(db.Model):
    __tablename__ = 'users'  # creating a table name
    user_id = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))

    @staticmethod
    def add_user(id, password):
        user = User(user_id=id, password=password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def find_user(id, password):
        user = User.query.filter_by(user_id=id).first()
        return user.user_id == id and user.password == password

    @staticmethod
    def login(id, password):
        user = User.query.filter_by(user_id=id).first()
        exists = user.user_id == id and user.password == password
        if exists:
            encoded = jwt.encode({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "user_id": id},
                                 key, algorithm="HS256")
            return encoded
        else:
            return "invalid credentials"

    @staticmethod
    def authenticate(token):
        try:
            decoded = jwt.decode(token, key, algorithms="HS256")["user_id"]
            user = User.query.filter_by(user_id=decoded).first()
            if not user:
                return False
            else:
                return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
