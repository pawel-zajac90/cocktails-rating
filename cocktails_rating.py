from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hyrybybydyby'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    from rating import rating as rating_blueprint

    app.register_blueprint(rating_blueprint)
    app.run(debug=True, port=8888)
